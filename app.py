from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Supabase 配置
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# 确保上传目录存在
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 最大文件大小

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/add')
def add_mistake_page():
    """添加错题页面"""
    return render_template('add_mistake.html')

@app.route('/list')
def list_mistakes_page():
    """错题列表页面"""
    return render_template('list_mistakes.html')

@app.route('/stats')
def stats_page():
    """统计页面"""
    return render_template('stats.html')

@app.route('/review/<mistake_id>')
def review_page(mistake_id):
    """复习页面"""
    return render_template('review.html', mistake_id=mistake_id)

# ==================== API 路由 ====================

@app.route('/api/knowledge-points', methods=['GET'])
def get_knowledge_points():
    """获取所有知识点"""
    try:
        result = supabase.table('knowledge_points').select('*').order('category').execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/question-types', methods=['GET'])
def get_question_types():
    """获取所有题型"""
    try:
        result = supabase.table('question_types').select('*').execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mistakes', methods=['GET'])
def get_mistakes():
    """获取错题列表，支持筛选"""
    try:
        query = supabase.table('mistakes').select('*, knowledge_points(name, category), question_types(name)')
        
        # 筛选参数
        knowledge_point_id = request.args.get('knowledge_point_id')
        question_type_id = request.args.get('question_type_id')
        mastery_level = request.args.get('mastery_level')
        
        if knowledge_point_id:
            query = query.eq('knowledge_point_id', knowledge_point_id)
        if question_type_id:
            query = query.eq('question_type_id', question_type_id)
        if mastery_level:
            query = query.eq('mastery_level', mastery_level)
        
        result = query.order('created_at', desc=True).execute()
        return jsonify({'success': True, 'data': result.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mistakes/<mistake_id>', methods=['GET'])
def get_mistake(mistake_id):
    """获取单个错题详情"""
    try:
        result = supabase.table('mistakes').select('*, knowledge_points(*), question_types(*)').eq('id', mistake_id).single().execute()
        
        # 获取复习记录
        review_logs = supabase.table('review_logs').select('*').eq('mistake_id', mistake_id).order('created_at', desc=True).execute()
        
        data = result.data
        data['review_logs'] = review_logs.data
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mistakes', methods=['POST'])
def create_mistake():
    """创建新错题"""
    try:
        data = request.form.to_dict()
        
        # 处理文件上传
        question_image = request.files.get('question_image')
        answer_image = request.files.get('answer_image')
        
        question_image_url = None
        answer_image_url = None
        
        if question_image:
            filename = f"question_{uuid.uuid4()}_{question_image.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            question_image.save(filepath)
            question_image_url = f"/static/uploads/{filename}"
        
        if answer_image:
            filename = f"answer_{uuid.uuid4()}_{answer_image.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            answer_image.save(filepath)
            answer_image_url = f"/static/uploads/{filename}"
        
        # 构建插入数据
        mistake_data = {
            'title': data.get('title'),
            'question_text': data.get('question_text'),
            'question_image_url': question_image_url,
            'answer_text': data.get('answer_text'),
            'answer_image_url': answer_image_url,
            'error_reason': data.get('error_reason'),
            'knowledge_point_id': data.get('knowledge_point_id'),
            'question_type_id': data.get('question_type_id'),
            'mastery_level': data.get('mastery_level', 'not_mastered'),
            'related_points': data.get('related_points', '').split(',') if data.get('related_points') else []
        }
        
        result = supabase.table('mistakes').insert(mistake_data).execute()
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mistakes/<mistake_id>', methods=['PUT'])
def update_mistake(mistake_id):
    """更新错题"""
    try:
        data = request.get_json()
        
        update_data = {
            'title': data.get('title'),
            'question_text': data.get('question_text'),
            'answer_text': data.get('answer_text'),
            'error_reason': data.get('error_reason'),
            'knowledge_point_id': data.get('knowledge_point_id'),
            'question_type_id': data.get('question_type_id'),
            'mastery_level': data.get('mastery_level'),
            'related_points': data.get('related_points', [])
        }
        
        result = supabase.table('mistakes').update(update_data).eq('id', mistake_id).execute()
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mistakes/<mistake_id>', methods=['DELETE'])
def delete_mistake(mistake_id):
    """删除错题"""
    try:
        supabase.table('mistakes').delete().eq('id', mistake_id).execute()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mistakes/<mistake_id>/review', methods=['POST'])
def add_review(mistake_id):
    """添加复习记录"""
    try:
        data = request.get_json()
        
        # 创建复习记录
        review_data = {
            'mistake_id': mistake_id,
            'review_notes': data.get('review_notes'),
            'mastery_level_after': data.get('mastery_level_after')
        }
        
        result = supabase.table('review_logs').insert(review_data).execute()
        
        # 更新错题的复习次数和掌握程度
        mistake_update = {
            'review_count': supabase.table('mistakes').select('review_count').eq('id', mistake_id).single().execute().data['review_count'] + 1,
            'last_reviewed_at': datetime.now().isoformat(),
            'mastery_level': data.get('mastery_level_after')
        }
        
        supabase.table('mistakes').update(mistake_update).eq('id', mistake_id).execute()
        
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计数据"""
    try:
        # 总错题数
        total_mistakes = supabase.table('mistakes').select('*', count='exact').execute().count
        
        # 按掌握程度统计
        mastery_stats = supabase.table('mistakes').select('mastery_level', count='exact').execute()
        mastery_data = {}
        for item in mastery_stats.data:
            level = item['mastery_level']
            mastery_data[level] = mastery_data.get(level, 0) + 1
        
        # 按知识点统计
        knowledge_stats = supabase.table('mistakes').select('knowledge_point_id, knowledge_points(name)').execute()
        knowledge_data = {}
        for item in knowledge_stats.data:
            name = item['knowledge_points']['name'] if item['knowledge_points'] else '未分类'
            knowledge_data[name] = knowledge_data.get(name, 0) + 1
        
        # 最近7天新增错题
        recent_mistakes = supabase.table('mistakes').select('*', count='exact').gte('created_at', 
            (datetime.now().timestamp() - 7*24*3600)).execute().count
        
        return jsonify({
            'success': True,
            'data': {
                'total_mistakes': total_mistakes,
                'mastery_stats': mastery_data,
                'knowledge_stats': knowledge_data,
                'recent_mistakes': recent_mistakes
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """提供上传的文件"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
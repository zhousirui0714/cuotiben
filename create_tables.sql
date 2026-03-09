-- 工科数学分析错题本数据库表结构
-- 在 Supabase SQL Editor 中执行

-- 1. 知识点分类表
CREATE TABLE IF NOT EXISTS knowledge_points (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 如：极限、导数、积分、级数等
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. 题型分类表
CREATE TABLE IF NOT EXISTS question_types (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. 错题表
CREATE TABLE IF NOT EXISTS mistakes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    question_text TEXT, -- 题目文本
    question_image_url TEXT, -- 题目图片URL
    answer_text TEXT, -- 解答文本
    answer_image_url TEXT, -- 解答图片URL
    error_reason TEXT NOT NULL, -- 错误原因
    knowledge_point_id UUID REFERENCES knowledge_points(id),
    question_type_id UUID REFERENCES question_types(id),
    mastery_level VARCHAR(20) DEFAULT 'not_mastered' CHECK (mastery_level IN ('not_mastered', 'reviewing', 'mastered')), -- 掌握程度
    related_points TEXT[], -- 关联考点（数组）
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    review_count INTEGER DEFAULT 0, -- 复习次数
    last_reviewed_at TIMESTAMP WITH TIME ZONE -- 最后复习时间
);

-- 4. 复习记录表
CREATE TABLE IF NOT EXISTS review_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    mistake_id UUID REFERENCES mistakes(id) ON DELETE CASCADE,
    review_notes TEXT, -- 复习笔记
    mastery_level_after VARCHAR(20) CHECK (mastery_level_after IN ('not_mastered', 'reviewing', 'mastered')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. 插入默认知识点数据
INSERT INTO knowledge_points (name, category, description) VALUES
('函数极限', '极限与连续', '函数在某点的极限概念与计算'),
('数列极限', '极限与连续', '数列极限的定义与性质'),
('连续性', '极限与连续', '函数的连续性与间断点'),
('导数定义', '导数与微分', '导数的定义与几何意义'),
('求导法则', '导数与微分', '基本求导公式与运算法则'),
('微分中值定理', '导数与微分', '罗尔定理、拉格朗日定理等'),
('不定积分', '积分学', '不定积分的概念与计算'),
('定积分', '积分学', '定积分的定义与性质'),
('重积分', '积分学', '二重积分与三重积分'),
('级数收敛', '级数', '数项级数的收敛判别法'),
('幂级数', '级数', '幂级数的收敛域与和函数'),
('傅里叶级数', '级数', '函数的傅里叶展开')
ON CONFLICT DO NOTHING;

-- 6. 插入默认题型数据
INSERT INTO question_types (name, description) VALUES
('计算题', '需要进行数学计算求解的题目'),
('证明题', '需要逻辑推理和证明的题目'),
('概念题', '考察概念理解的题目'),
('应用题', '实际应用场景的数学建模题'),
('选择题', '从选项中选择正确答案'),
('填空题', '填写正确答案的题目')
ON CONFLICT DO NOTHING;

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_mistakes_knowledge_point ON mistakes(knowledge_point_id);
CREATE INDEX IF NOT EXISTS idx_mistakes_question_type ON mistakes(question_type_id);
CREATE INDEX IF NOT EXISTS idx_mistakes_mastery_level ON mistakes(mastery_level);
CREATE INDEX IF NOT EXISTS idx_mistakes_created_at ON mistakes(created_at);
CREATE INDEX IF NOT EXISTS idx_review_logs_mistake_id ON review_logs(mistake_id);

-- 启用行级安全性 (RLS)
ALTER TABLE knowledge_points ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_types ENABLE ROW LEVEL SECURITY;
ALTER TABLE mistakes ENABLE ROW LEVEL SECURITY;
ALTER TABLE review_logs ENABLE ROW LEVEL SECURITY;

-- 创建 RLS 策略 - 允许所有操作（简化版，实际应用应该根据用户身份限制）
CREATE POLICY "允许所有操作" ON knowledge_points FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "允许所有操作" ON question_types FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "允许所有操作" ON mistakes FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "允许所有操作" ON review_logs FOR ALL USING (true) WITH CHECK (true);

-- 创建更新时间戳的函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为 mistakes 表创建触发器
DROP TRIGGER IF EXISTS update_mistakes_updated_at ON mistakes;
CREATE TRIGGER update_mistakes_updated_at 
    BEFORE UPDATE ON mistakes 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 查询创建的表结构
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name IN ('knowledge_points', 'question_types', 'mistakes', 'review_logs')
ORDER BY table_name, ordinal_position;
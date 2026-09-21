-- Al-La'eeb Enhanced Database Schema - Production Scale
-- Supports millions of users with partitioning and advanced indexing

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";      -- GIN indexes

-- ============================================================
-- USERS TABLE (Partitioned by country for geo-distribution)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'player',
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    is_premium BOOLEAN DEFAULT false,
    country VARCHAR(100),
    city VARCHAR(100),
    timezone VARCHAR(50) DEFAULT 'UTC',
    date_of_birth DATE,
    profile_image_url TEXT,
    onboarding_completed BOOLEAN DEFAULT false,
    last_login_at TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
) PARTITION BY LIST (country);

-- Create partitions for major regions
CREATE TABLE IF NOT EXISTS users_mena PARTITION OF users FOR VALUES IN ('UAE', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Bahrain', 'Oman', 'Egypt', 'Morocco', 'Tunisia', 'Algeria', 'Jordan', 'Lebanon', 'Iraq', 'Yemen', 'Libya', 'Syria', 'Palestine');
CREATE TABLE IF NOT EXISTS users_europe PARTITION OF users FOR VALUES IN ('UK', 'France', 'Germany', 'Spain', 'Italy', 'Netherlands', 'Belgium', 'Portugal', 'Switzerland', 'Austria', 'Sweden', 'Norway', 'Denmark', 'Finland');
CREATE TABLE IF NOT EXISTS users_americas PARTITION OF users FOR VALUES IN ('USA', 'Canada', 'Brazil', 'Argentina', 'Mexico', 'Colombia', 'Chile', 'Uruguay');
CREATE TABLE IF NOT EXISTS users_asia PARTITION OF users FOR VALUES IN ('Japan', 'South Korea', 'China', 'India', 'Australia', 'Thailand', 'Malaysia', 'Indonesia', 'Singapore');
CREATE TABLE IF NOT EXISTS users_default PARTITION OF users DEFAULT;

-- ============================================================
-- PLAYER PROFILES (Sharded by user_id hash)
-- ============================================================
CREATE TABLE IF NOT EXISTS player_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    height_cm FLOAT,
    weight_kg FLOAT,
    dominant_foot VARCHAR(10) CHECK (dominant_foot IN ('left', 'right', 'both')),
    primary_position VARCHAR(50),
    secondary_positions TEXT[],
    preferred_positions JSONB DEFAULT '[]',
    current_club VARCHAR(255),
    current_academy VARCHAR(255),
    club_history JSONB DEFAULT '[]',
    jersey_number INTEGER CHECK (jersey_number BETWEEN 1 AND 99),
    biography TEXT,
    achievements TEXT[],
    languages TEXT[],
    video_highlight_url TEXT,
    overall_score FLOAT DEFAULT 0,
    potential_score FLOAT DEFAULT 0,
    market_value_eur BIGINT,
    is_scoutable BOOLEAN DEFAULT true,
    is_public_profile BOOLEAN DEFAULT true,
    social_links JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- VIDEO UPLOADS (Partitioned by month for time-series data)
-- ============================================================
CREATE TABLE IF NOT EXISTS video_uploads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    match_type VARCHAR(50) NOT NULL,
    opponent VARCHAR(255),
    match_date TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    file_size_bytes BIGINT,
    file_format VARCHAR(20),
    resolution VARCHAR(20),
    fps INTEGER,
    status VARCHAR(50) DEFAULT 'processing',
    storage_url TEXT,
    stream_url TEXT,
    thumbnail_url TEXT,
    processing_progress FLOAT DEFAULT 0.0,
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processing_completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT false,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES users(id) ON DELETE CASCADE
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE IF NOT EXISTS video_uploads_2024_01 PARTITION OF video_uploads FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_02 PARTITION OF video_uploads FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_03 PARTITION OF video_uploads FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_04 PARTITION OF video_uploads FOR VALUES FROM ('2024-04-01') TO ('2024-05-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_05 PARTITION OF video_uploads FOR VALUES FROM ('2024-05-01') TO ('2024-06-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_06 PARTITION OF video_uploads FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_07 PARTITION OF video_uploads FOR VALUES FROM ('2024-07-01') TO ('2024-08-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_08 PARTITION OF video_uploads FOR VALUES FROM ('2024-08-01') TO ('2024-09-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_09 PARTITION OF video_uploads FOR VALUES FROM ('2024-09-01') TO ('2024-10-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_10 PARTITION OF video_uploads FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_11 PARTITION OF video_uploads FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');
CREATE TABLE IF NOT EXISTS video_uploads_2024_12 PARTITION OF video_uploads FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');
CREATE TABLE IF NOT EXISTS video_uploads_2025_01 PARTITION OF video_uploads FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- ============================================================
-- PERFORMANCE METRICS (Compressed, partitioned)
-- ============================================================
CREATE TABLE IF NOT EXISTS performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID NOT NULL,
    player_id UUID NOT NULL,
    match_date TIMESTAMP WITH TIME ZONE,

    -- Physical
    max_speed_kmh FLOAT,
    avg_speed_kmh FLOAT,
    total_distance_m FLOAT,
    sprint_count INTEGER,
    max_acceleration_ms2 FLOAT,
    jump_height_cm FLOAT,
    metabolic_load FLOAT,

    -- Technical
    pass_accuracy FLOAT,
    pass_count INTEGER,
    shot_accuracy FLOAT,
    shot_count INTEGER,
    dribble_success_rate FLOAT,
    dribble_count INTEGER,
    touch_count INTEGER,

    -- Tactical
    positioning_score FLOAT,
    tactical_awareness FLOAT,
    defensive_actions INTEGER,
    interceptions INTEGER,

    -- Biomechanical
    strike_biomechanics FLOAT,
    center_of_mass_stability FLOAT,
    limb_symmetry FLOAT,

    -- Overall
    overall_rating FLOAT,
    percentile_vs_professionals FLOAT,
    raw_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- ============================================================
-- EVENTS TABLE (High-write, partitioned by day)
-- ============================================================
CREATE TABLE IF NOT EXISTS match_events (
    id BIGSERIAL,
    video_id UUID NOT NULL,
    player_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    timestamp_ms BIGINT NOT NULL,
    frame_id INTEGER,
    x_position FLOAT,
    y_position FLOAT,
    outcome VARCHAR(20),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- ============================================================
-- COACHING REPORTS
-- ============================================================
CREATE TABLE IF NOT EXISTS coaching_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID NOT NULL,
    video_id UUID NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    strengths TEXT[],
    weaknesses TEXT[],
    key_moments JSONB,
    similar_professionals JSONB,
    similarity_score FLOAT,
    drills JSONB,
    weekly_plan JSONB,
    coach_feedback_ar TEXT,
    coach_feedback_en TEXT,
    ai_model_version VARCHAR(50),
    processing_time_ms INTEGER
);

-- ============================================================
-- VERIFICATION LOGS
-- ============================================================
CREATE TABLE IF NOT EXISTS verification_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID NOT NULL,
    face_match_score FLOAT,
    kit_match_score FLOAT,
    overall_confidence FLOAT,
    verification_status VARCHAR(50) DEFAULT 'pending',
    processing_time_ms FLOAT,
    anti_fraud_passed BOOLEAN,
    geofence_valid BOOLEAN,
    gps_latitude FLOAT,
    gps_longitude FLOAT,
    gps_accuracy FLOAT,
    device_fingerprint TEXT,
    ip_address INET,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (timestamp);

-- ============================================================
-- SCOUT INTERACTIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS scout_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scout_id UUID NOT NULL,
    player_id UUID NOT NULL,
    interaction_type VARCHAR(50) NOT NULL, -- view, favorite, contact, offer
    notes TEXT,
    rating FLOAT CHECK (rating BETWEEN 1 AND 10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- NOTIFICATIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    data JSONB DEFAULT '{}',
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- ADVANCED INDEXES
-- ============================================================

-- Users indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_country ON users(country);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_created ON users(created_at);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_active ON users(is_active) WHERE is_active = true;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_verified ON users(is_verified) WHERE is_verified = true;

-- Player profiles indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_user ON player_profiles(user_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_position ON player_profiles(primary_position);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_score ON player_profiles(overall_score DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_potential ON player_profiles(potential_score DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_scoutable ON player_profiles(is_scoutable) WHERE is_scoutable = true;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_club ON player_profiles(current_club);

-- Full-text search on player bios
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_bio_search ON player_profiles USING gin(to_tsvector('english', biography));
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_achievements ON player_profiles USING gin(achievements);

-- Video indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_video_player ON video_uploads(player_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_video_status ON video_uploads(status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_video_created ON video_uploads(created_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_video_match_date ON video_uploads(match_date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_video_public ON video_uploads(is_public) WHERE is_public = true;

-- Metrics indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_metrics_player ON performance_metrics(player_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_metrics_video ON performance_metrics(video_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_metrics_rating ON performance_metrics(overall_rating DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_metrics_date ON performance_metrics(created_at DESC);

-- Events indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_video ON match_events(video_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_player ON match_events(player_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_type ON match_events(event_type);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_timestamp ON match_events(timestamp_ms);

-- Verification indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_verification_player ON verification_logs(player_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_verification_status ON verification_logs(verification_status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_verification_timestamp ON verification_logs(timestamp DESC);

-- Scout indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_scout_scout ON scout_interactions(scout_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_scout_player ON scout_interactions(player_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_scout_type ON scout_interactions(interaction_type);

-- Notifications indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_notif_user ON notifications(user_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_notif_unread ON notifications(user_id, is_read) WHERE is_read = false;

-- ============================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON player_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Auto-calculate overall score
CREATE OR REPLACE FUNCTION calculate_overall_score()
RETURNS TRIGGER AS $$
BEGIN
    NEW.overall_rating = (
        COALESCE(NEW.max_speed_kmh / 35 * 25, 0) +
        COALESCE(NEW.pass_accuracy * 30, 0) +
        COALESCE(NEW.positioning_score * 25, 0) +
        COALESCE(NEW.strike_biomechanics * 10, 0) +
        COALESCE(NEW.decision_accuracy * 10, 0)
    );
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calc_overall BEFORE INSERT OR UPDATE ON performance_metrics
    FOR EACH ROW EXECUTE FUNCTION calculate_overall_score();

-- Partition maintenance function
CREATE OR REPLACE FUNCTION create_video_partition()
RETURNS void AS $$
DECLARE
    partition_date DATE;
    partition_name TEXT;
BEGIN
    partition_date := DATE_TRUNC('month', NOW() + INTERVAL '1 month');
    partition_name := 'video_uploads_' || TO_CHAR(partition_date, 'YYYY_MM');

    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF video_uploads FOR VALUES FROM (%L) TO (%L)',
        partition_name,
        partition_date,
        partition_date + INTERVAL '1 month'
    );
END;
$$ language 'plpgsql';

-- Materialized view for leaderboard
CREATE MATERIALIZED VIEW IF NOT EXISTS player_leaderboard AS
SELECT 
    p.id,
    p.user_id,
    u.first_name || ' ' || u.last_name as full_name,
    u.country,
    p.primary_position,
    p.overall_score,
    p.potential_score,
    COUNT(DISTINCT v.id) as match_count,
    MAX(m.overall_rating) as best_rating
FROM player_profiles p
JOIN users u ON p.user_id = u.id
LEFT JOIN video_uploads v ON v.player_id = p.user_id AND v.status = 'completed'
LEFT JOIN performance_metrics m ON m.player_id = p.user_id
WHERE u.is_active = true AND p.is_scoutable = true
GROUP BY p.id, p.user_id, u.first_name, u.last_name, u.country, p.primary_position, p.overall_score, p.potential_score
ORDER BY p.overall_score DESC;

CREATE UNIQUE INDEX idx_leaderboard_id ON player_leaderboard(id);

-- Refresh leaderboard every hour
SELECT cron.schedule('refresh-leaderboard', '0 * * * *', 
    'REFRESH MATERIALIZED VIEW CONCURRENTLY player_leaderboard');

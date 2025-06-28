# Configuration file for Real-Time Face Emotion Avatar

# Camera settings
CAMERA_SETTINGS = {
    'width': 640,
    'height': 480,
    'fps': 30,
    'flip_horizontal': True
}

# Emotion detection thresholds
EMOTION_THRESHOLDS = {
    'happy': {
        'mouth_stretch_min': 0.40,
        'mouth_open_max': 0.06
    },
    'surprise': {
        'mouth_open_min': 0.12
    },
    'fear': {
        'mouth_open_min': 0.06,
        'mouth_open_max': 0.12,
        'eyebrow_height_min': 0.05
    },
    'sad': {
        'sad_offset_min': 0.01,
        'eye_open_max': 0.04
    },
    'disgust': {
        'mouth_open_max': 0.03,
        'mouth_stretch_max': 0.38
    },
    'angry': {
        'eye_open_min': 0.096,
        'mouth_open_max': 0.06
    }
}

# UI settings
UI_SETTINGS = {
    'window_width': 640,
    'window_height': 480,
    'font_scale': 1.2,
    'font_thickness': 3,
    'text_color': (255, 255, 255),
    'background_color': (0, 0, 0)
}

# Avatar styles
AVATAR_STYLES = {
    'mesh': {
        'name': 'Full Mesh',
        'description': 'Detailed facial mesh with all landmarks'
    },
    'points': {
        'name': 'Points',
        'description': 'Minimal point-based visualization'
    },
    'minimal': {
        'name': 'Minimal',
        'description': 'Clean contour-based outline'
    }
}

# Performance settings
PERFORMANCE_SETTINGS = {
    'max_fps_history': 10,
    'max_emotion_history': 30,
    'detection_confidence': 0.5,
    'tracking_confidence': 0.5
}

# File paths
PATHS = {
    'screenshots_dir': 'screenshots',
    'logs_dir': 'logs'
}

# Debug settings
DEBUG_SETTINGS = {
    'show_feature_values': False,
    'show_emotion_scores': False,
    'show_performance_metrics': True
} 
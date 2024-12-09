# System Architecture

This document describes the architecture of the Tesla Vision Simulator project.

## High-Level Architecture

```mermaid
flowchart TD
    subgraph Input
        A[Vehicle Camera Feed] --> B[Video Stream Handler]
    end

    subgraph ComputerVision["Computer Vision Pipeline (GPU)"]
        B --> C[Frame Preprocessor]
        C --> D[YOLOv9 Object Detection]
        C --> E[Lane Detection Model]
        D --> F[Object Tracking]
        E --> G[Road Feature Extractor]
    end

    subgraph DataProcessing["Data Processing Layer"]
        F --> H[Object Metadata Generator]
        G --> H
        H --> I[Scene Composition Logic]
    end

    subgraph BlenderEngine["Blender Environment"]
        I --> J[Scene Generator]
        K[(3D Model Library)] --> J
        J --> L[Real-time Renderer]
    end

    subgraph CloudInfra["Google Cloud Vertex AI"]
        M[Model Serving API]
        N[Load Balancer]
        O[Monitoring Service]
        P[Storage]
    end

    B --> M
    M --> C
    N --> M
    H --> P
    L --> O
```

## Components Description

### Input Layer
- **Vehicle Camera Feed**: Raw input from the front-facing camera
- **Video Stream Handler**: Manages real-time video stream and frame extraction

### Computer Vision Pipeline
- **Frame Preprocessor**: Normalizes and prepares frames for models
- **YOLOv9**: Handles object detection (vehicles, pedestrians, signs)
- **Lane Detection Model**: Processes road markings and lanes
- **Object Tracking**: Maintains object consistency across frames
- **Road Feature Extractor**: Analyzes road geometry and features

### Data Processing Layer
- **Object Metadata Generator**: Converts detections to 3D scene metadata
- **Scene Composition Logic**: Orchestrates scene elements and transformations

### Blender Environment
- **3D Model Library**: Pre-loaded assets (vehicles, infrastructure)
- **Scene Generator**: Creates dynamic 3D environment
- **Real-time Renderer**: Renders final output

### Cloud Infrastructure
- **Model Serving API**: Handles model inference
- **Load Balancer**: Distributes processing load
- **Monitoring Service**: Tracks performance metrics
- **Storage**: Manages assets and temporary data

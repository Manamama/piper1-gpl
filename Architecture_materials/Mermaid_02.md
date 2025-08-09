graph TD;
    subgraph Build Flow
        direction LR;
        pip(pip install .) --> setup_py["setup.py(scikit-build)"];
        setup_py --> cmake["CMake"];
        cmake --> cmakelists["CMakeLists.txt"];
    end

    subgraph "Platform Logic (in CMakeLists.txt)"
        cmakelists --> plat_choice{Platform?};

        plat_choice -- "WIN32" --> win_path["Windows Path"];
        plat_choice -- "ANDROID" --> android_path["Android Path"];
        plat_choice -- "UNIX" --> unix_path["Generic Unix Path"];

        subgraph "Windows Build"
            direction TB;
            win_path --> win_espeak["Build espeak-ng from source (STATIC .lib)"];
            win_espeak --> win_link["Statically link espeak-ng into espeakbridge.pyd"];
            win_path --> win_onnx_missing["<font color=red><b>Missing:</b></font> No onnxruntime link"];
        end

        subgraph "Android (Termux) Build"
            direction TB;
            android_path --> termux_deps["Use 'pkg' to install python-onnxruntime"];
            termux_deps --> termux_find_onnx["Find system libonnxruntime.so"];
            android_path --> android_espeak["Build espeak-ng from source (SHARED .so)"];
            android_espeak --> android_link["Dynamically link espeakbridge.so to private libespeak-ng.so"];
            termux_find_onnx --> android_link;
        end

        subgraph "Generic Unix (Linux/macOS) Build"
            direction TB;
            unix_path --> unix_espeak["Build espeak-ng from source (STATIC .a)"];
            unix_espeak --> unix_link["Statically link espeak-ng into espeakbridge.so"];
            unix_path --> unix_onnx_missing["<font color=red><b>Missing:</b></font> No onnxruntime link"];
        end
    end

    subgraph Final Components
        direction TB
        win_link --> final_bridge_win["espeakbridge.pyd"];
        android_link --> final_bridge_android["espeakbridge.so"];
        unix_link --> final_bridge_unix["espeakbridge.so"];
    end

    classDef buildTool fill:#f9f,stroke:#333,stroke-width:2px;
    classDef component fill:#bbf,stroke:#333,stroke-width:2px;
    classDef logic fill:#e7c28d,stroke:#333,stroke-width:2px;
    classDef missing fill:#ffcccc,stroke:#cc0000,stroke-width:2px;

    class pip,cmake,setup_py buildTool;
    class cmakelists,plat_choice logic;
    class final_bridge_win,final_bridge_android,final_bridge_unix component;
    class win_onnx_missing,unix_onnx_missing missing;
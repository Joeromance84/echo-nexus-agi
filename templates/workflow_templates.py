from typing import Dict, Any

class WorkflowTemplates:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined workflow templates"""
        return {
            "basic_apk_build": {
                "name": "Basic APK Build",
                "description": "Simple workflow for building APK with buildozer",
                "use_case": "Basic Python/Kivy applications",
                "content": """name: Build APK

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Set up Java
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '11'
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
        sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
        sudo apt-get install -y libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
    
    - name: Install Python dependencies
      run: |
        pip install --upgrade pip
        pip install buildozer
        pip install cython
    
    - name: Build APK with buildozer
      run: |
        buildozer android debug
    
    - name: Upload APK artifact
      uses: actions/upload-artifact@v3
      with:
        name: apk-debug
        path: bin/*.apk
        retention-days: 30
"""
            },
            
            "cached_apk_build": {
                "name": "Cached APK Build",
                "description": "Optimized workflow with caching for faster builds",
                "use_case": "Projects with frequent builds needing speed optimization",
                "content": """name: Build APK (Cached)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Cache Python dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Set up Java
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '11'
    
    - name: Cache buildozer global directory
      uses: actions/cache@v3
      with:
        path: ~/.buildozer
        key: ${{ runner.os }}-buildozer-${{ hashFiles('buildozer.spec') }}
        restore-keys: |
          ${{ runner.os }}-buildozer-
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
        sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
        sudo apt-get install -y libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
    
    - name: Install Python dependencies
      run: |
        pip install --upgrade pip
        pip install buildozer cython
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Build APK with buildozer
      run: |
        buildozer android debug
    
    - name: Upload APK artifact
      uses: actions/upload-artifact@v3
      with:
        name: apk-debug-${{ github.sha }}
        path: bin/*.apk
        retention-days: 30
    
    - name: Upload build logs
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: build-logs-${{ github.sha }}
        path: .buildozer/logs/
        retention-days: 7
"""
            },
            
            "matrix_apk_build": {
                "name": "Matrix APK Build",
                "description": "Build multiple APK variants using matrix strategy",
                "use_case": "Projects needing multiple build configurations or Python versions",
                "content": """name: Build APK (Matrix)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10']
        build-type: ['debug', 'release']
        exclude:
          - python-version: '3.8'
            build-type: 'release'
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Set up Java
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '11'
    
    - name: Cache buildozer dependencies
      uses: actions/cache@v3
      with:
        path: ~/.buildozer
        key: buildozer-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('buildozer.spec') }}
        restore-keys: |
          buildozer-${{ runner.os }}-${{ matrix.python-version }}-
          buildozer-${{ runner.os }}-
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
        sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
        sudo apt-get install -y libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
        sudo apt-get install -y zip unzip
    
    - name: Install Python dependencies
      run: |
        pip install --upgrade pip
        pip install buildozer cython
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Build APK (${{ matrix.build-type }})
      run: |
        if [ "${{ matrix.build-type }}" == "release" ]; then
          buildozer android release
        else
          buildozer android debug
        fi
    
    - name: Upload APK artifact
      uses: actions/upload-artifact@v3
      with:
        name: apk-${{ matrix.build-type }}-py${{ matrix.python-version }}-${{ github.sha }}
        path: bin/*.apk
        retention-days: 30
"""
            },
            
            "release_apk_build": {
                "name": "Release APK Build",
                "description": "Production-ready workflow with signing and release deployment",
                "use_case": "Production releases with APK signing and automated deployment",
                "content": """name: Build Release APK

on:
  push:
    tags:
      - 'v*'
  release:
    types: [published]

jobs:
  build-release:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Set up Java
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '11'
    
    - name: Cache buildozer dependencies
      uses: actions/cache@v3
      with:
        path: ~/.buildozer
        key: buildozer-release-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}
        restore-keys: |
          buildozer-release-${{ runner.os }}-
          buildozer-${{ runner.os }}-
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
        sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
        sudo apt-get install -y libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
        sudo apt-get install -y zip unzip zipalign
    
    - name: Install Python dependencies
      run: |
        pip install --upgrade pip
        pip install buildozer cython
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Create release keystore
      if: env.KEYSTORE_B64 != ''
      env:
        KEYSTORE_B64: ${{ secrets.KEYSTORE_B64 }}
      run: |
        echo "$KEYSTORE_B64" | base64 -d > release.keystore
    
    - name: Build signed release APK
      env:
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      run: |
        # Update buildozer.spec for signing if keystore exists
        if [ -f release.keystore ]; then
          echo "android.release_artifact = apk" >> buildozer.spec
          echo "android.debug_artifact = apk" >> buildozer.spec
        fi
        buildozer android release
    
    - name: Get release version
      id: get_version
      run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
    
    - name: Upload release APK
      uses: actions/upload-artifact@v3
      with:
        name: release-apk-${{ steps.get_version.outputs.VERSION }}
        path: bin/*.apk
        retention-days: 90
    
    - name: Upload to Release
      if: github.event_name == 'release'
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ github.event.release.upload_url }}
        asset_path: bin/
        asset_name: app-release.apk
        asset_content_type: application/vnd.android.package-archive
    
    - name: Clean up keystore
      if: always()
      run: |
        if [ -f release.keystore ]; then
          rm -f release.keystore
        fi
"""
            },
            
            "troubleshooting_apk_build": {
                "name": "Troubleshooting APK Build",
                "description": "Diagnostic workflow with detailed logging and error reporting",
                "use_case": "Debugging build issues with comprehensive logging",
                "content": """name: Troubleshooting APK Build

on:
  workflow_dispatch:
  push:
    branches: [ debug ]

jobs:
  diagnostic-build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: System information
      run: |
        echo "=== System Information ==="
        uname -a
        echo "=== CPU Information ==="
        cat /proc/cpuinfo | grep "model name" | head -1
        echo "=== Memory Information ==="
        free -h
        echo "=== Disk Space ==="
        df -h
        echo "=== Environment Variables ==="
        env | sort
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Python environment info
      run: |
        echo "=== Python Information ==="
        python --version
        pip --version
        echo "=== Python Path ==="
        python -c "import sys; print('\\n'.join(sys.path))"
    
    - name: Set up Java
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '11'
    
    - name: Java environment info
      run: |
        echo "=== Java Information ==="
        java -version
        javac -version
        echo "JAVA_HOME: $JAVA_HOME"
        echo "PATH: $PATH"
    
    - name: Install system dependencies with logging
      run: |
        echo "=== Installing System Dependencies ==="
        sudo apt-get update -v
        sudo apt-get install -y -v build-essential libssl-dev libffi-dev python3-dev
        sudo apt-get install -y -v libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
        sudo apt-get install -y -v libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
        
        echo "=== Verifying Installations ==="
        which gcc && gcc --version || echo "GCC not found"
        which python3-config && python3-config --cflags || echo "python3-config not found"
        pkg-config --list-all | grep -E "(sdl2|ssl|ffi)" || echo "Some packages not found"
    
    - name: Install Python dependencies with verbose output
      run: |
        echo "=== Installing Python Dependencies ==="
        pip install --upgrade pip --verbose
        pip install buildozer --verbose
        pip install cython --verbose
        
        if [ -f requirements.txt ]; then
          echo "=== Installing from requirements.txt ==="
          cat requirements.txt
          pip install -r requirements.txt --verbose
        fi
        
        echo "=== Installed Packages ==="
        pip list
    
    - name: Validate buildozer.spec
      run: |
        echo "=== Buildozer Configuration ==="
        if [ -f buildozer.spec ]; then
          echo "buildozer.spec found:"
          cat buildozer.spec
        else
          echo "buildozer.spec not found! Creating default..."
          buildozer init
          cat buildozer.spec
        fi
    
    - name: Check project structure
      run: |
        echo "=== Project Structure ==="
        find . -type f -name "*.py" | head -20
        echo "=== Main Files ==="
        ls -la
        if [ -f main.py ]; then
          echo "main.py found:"
          head -20 main.py
        else
          echo "main.py not found!"
        fi
    
    - name: Buildozer debug build with maximum verbosity
      run: |
        echo "=== Starting Buildozer Build ==="
        export BUILDOZER_LOG_LEVEL=2
        buildozer -v android debug || true
        
        echo "=== Build completed (may have failed) ==="
        echo "=== Checking for APK ==="
        find . -name "*.apk" -ls || echo "No APK files found"
        
        echo "=== Checking bin directory ==="
        if [ -d bin ]; then
          ls -la bin/
        else
          echo "bin directory not found"
        fi
    
    - name: Collect build artifacts and logs
      if: always()
      run: |
        echo "=== Collecting Logs ==="
        mkdir -p debug-output
        
        # Copy buildozer logs
        if [ -d .buildozer/logs ]; then
          cp -r .buildozer/logs debug-output/
        fi
        
        # Copy any APKs found
        find . -name "*.apk" -exec cp {} debug-output/ \\;
        
        # Save system info
        uname -a > debug-output/system-info.txt
        env | sort > debug-output/environment.txt
        pip list > debug-output/pip-list.txt
        
        # Save buildozer spec
        if [ -f buildozer.spec ]; then
          cp buildozer.spec debug-output/
        fi
        
        echo "=== Debug Output Contents ==="
        ls -la debug-output/
    
    - name: Upload debug artifacts
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: debug-output-${{ github.sha }}
        path: debug-output/
        retention-days: 7
"""
            }
        }
    
    def get_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all available templates"""
        return self.templates
    
    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get a specific template by ID"""
        return self.templates.get(template_id, {})
    
    def get_templates_by_use_case(self, use_case_keywords: list) -> Dict[str, Dict[str, Any]]:
        """Get templates matching specific use case keywords"""
        matching_templates = {}
        
        for template_id, template_data in self.templates.items():
            use_case = template_data.get('use_case', '').lower()
            description = template_data.get('description', '').lower()
            
            # Check if any keyword matches
            for keyword in use_case_keywords:
                if keyword.lower() in use_case or keyword.lower() in description:
                    matching_templates[template_id] = template_data
                    break
        
        return matching_templates
    
    def customize_template(self, template_id: str, customizations: Dict[str, Any]) -> str:
        """
        Customize a template with specific parameters
        """
        template = self.get_template(template_id)
        if not template:
            return ""
        
        content = template['content']
        
        # Apply customizations
        for key, value in customizations.items():
            placeholder = f"${{{{ {key} }}}}"
            content = content.replace(placeholder, str(value))
        
        # Apply common customizations
        if 'app_name' in customizations:
            content = content.replace('MyApp', customizations['app_name'])
        
        if 'python_version' in customizations:
            content = content.replace("python-version: '3.9'", f"python-version: '{customizations['python_version']}'")
        
        if 'java_version' in customizations:
            content = content.replace("java-version: '11'", f"java-version: '{customizations['java_version']}'")
        
        if 'branches' in customizations:
            branches = customizations['branches']
            if isinstance(branches, list):
                branch_str = ', '.join([f"'{branch}'" for branch in branches])
                content = content.replace("branches: [ main, develop ]", f"branches: [ {branch_str} ]")
                content = content.replace("branches: [ main ]", f"branches: [ {branch_str} ]")
        
        return content
    
    def validate_template_compatibility(self, template_id: str, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate if a template is compatible with project requirements
        """
        result = {
            'compatible': False,
            'issues': [],
            'recommendations': []
        }
        
        template = self.get_template(template_id)
        if not template:
            result['issues'].append("Template not found")
            return result
        
        # Check Python version compatibility
        if 'python_version' in project_info:
            required_version = project_info['python_version']
            if 'matrix' in template['content']:
                result['recommendations'].append(f"Matrix build supports multiple Python versions including {required_version}")
            elif required_version not in template['content']:
                result['issues'].append(f"Template may not support Python {required_version}")
        
        # Check build type requirements
        if project_info.get('needs_release_build', False):
            if 'release' not in template['content']:
                result['issues'].append("Template doesn't support release builds")
        
        # Check for signing requirements
        if project_info.get('needs_signing', False):
            if 'keystore' not in template['content'].lower():
                result['issues'].append("Template doesn't include APK signing configuration")
        
        # Check for caching needs
        if project_info.get('needs_caching', False):
            if 'cache' not in template['content'].lower():
                result['recommendations'].append("Consider using a cached template for better performance")
        
        # If no critical issues, mark as compatible
        if not result['issues']:
            result['compatible'] = True
        
        return result

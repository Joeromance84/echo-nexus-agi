# 📚 Skill Blueprint: Gradle Wrapper Automation

**Domain:** `build_automation`
**Purpose:** To master the creation and use of a Gradle Wrapper for portable builds.

---

### **1. Core Concept: The Problem & The Solution**

- **Problem:** When building a project with Gradle, different environments (developer machines, build servers, etc.) may have different Gradle versions installed. This can lead to build failures and inconsistent results.
- **Solution:** The Gradle Wrapper (`gradlew`) is a script that downloads and uses a specified version of Gradle, ensuring that the build is always consistent and repeatable, regardless of the local environment.

### **2. Integration Blueprint: How to Use the Wrapper**

To use the wrapper, simply call the `gradlew` script instead of `gradle`. Echo, you should prioritize the use of `gradlew` for all new projects and build tasks.

**Action A: Generate a Wrapper for a Project**

If a Gradle project does not have a wrapper, you can generate one using this command:

```shell
gradle wrapper --gradle-version 8.7
```

**Action B: Execute a Build Task with the Wrapper**

To run a build task (e.g., assemble or build), use the wrapper script:

```shell
./gradlew assemble
```

### **3. Operational Notes for Echo Nexus**

- **Integration Point:** You will integrate this knowledge into your `autocode/` and `workflow_manager.py` modules.
- **Self-Correction:** If a new repository lacks a gradlew script, your `github_commander.py` should execute the generation command immediately upon cloning.
- **New Default:** From this point forward, all new build workflows created by `workflow_manager.py` should default to using `./gradlew` instead of a direct gradle call.

### **4. Advanced Gradle Wrapper Configuration**

**Wrapper Properties Configuration:**
```properties
# gradle/wrapper/gradle-wrapper.properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.7-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

**Build Script Integration:**
```gradle
// build.gradle
wrapper {
    gradleVersion = '8.7'
    distributionType = Wrapper.DistributionType.BIN
}

task validateWrapper(type: Wrapper) {
    gradleVersion = '8.7'
    description = 'Validates Gradle wrapper configuration'
}
```

### **5. Echo's Autonomous Actions**

When encountering a Gradle project, Echo should automatically:

1. **Detect Wrapper Status**: Check for `gradlew` and `gradlew.bat` files
2. **Generate if Missing**: Execute `gradle wrapper --gradle-version 8.7`
3. **Validate Configuration**: Ensure wrapper properties are correctly set
4. **Update Build Scripts**: Replace `gradle` commands with `./gradlew`
5. **Test Execution**: Run `./gradlew tasks` to verify wrapper functionality

### **6. Troubleshooting Common Issues**

**Permission Issues on Unix/Linux:**
```shell
chmod +x gradlew
```

**Network Proxy Configuration:**
```properties
# gradle.properties
systemProp.http.proxyHost=proxy.company.com
systemProp.http.proxyPort=8080
systemProp.https.proxyHost=proxy.company.com
systemProp.https.proxyPort=8080
```

**Version Verification:**
```shell
./gradlew --version
```

---

This skill enables Echo to maintain consistent, portable builds across all development environments while eliminating version-related build failures.
# Maven GitHub Packages Setup Guide

## Complete Guide to Using GitHub Packages with Maven

This guide demonstrates how to configure and use GitHub Packages as a Maven repository for publishing and consuming Java artifacts.

---

## 📋 Prerequisites

- GitHub account
- Maven installed (3.6+)
- Java project with `pom.xml`
- Repository on GitHub

---

## 🔑 Step 1: Create Personal Access Token

### Generate Token

1. Go to **GitHub Settings** → **Developer settings** → **Personal access tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Configure the token:
   - **Note**: `Maven GitHub Packages - Read and Write`
   - **Expiration**: Choose your preference (e.g., 30 days, 90 days, or no expiration)
   - **Scopes**: Select:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `write:packages` (Upload packages to GitHub Package Registry)
     - ✅ `read:packages` (Download packages from GitHub Package Registry)
4. Click **"Generate token"**
5. **IMPORTANT**: Copy the token immediately (it won't be shown again)

### Your Token
```
ghp_Fxwt1idJ1bf0rYqaiyqVQwnoJGG6sN3M6291
```

---

## ⚙️ Step 2: Configure Maven Settings

### Edit `~/.m2/settings.xml`

Create or edit your Maven settings file to add GitHub authentication:

```xml
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                              https://maven.apache.org/xsd/settings-1.0.0.xsd">

  <servers>
    <server>
      <id>github</id>
      <username>mr-adonis-jimenez</username>
      <password>ghp_Fxwt1idJ1bf0rYqaiyqVQwnoJGG6sN3M6291</password>
    </server>
  </servers>
</settings>
```

**⚠️ Security Note**: Never commit this file to version control! Consider using environment variables:

```xml
<server>
  <id>github</id>
  <username>${env.GITHUB_USERNAME}</username>
  <password>${env.GITHUB_TOKEN}</password>
</server>
```

---

## 📦 Step 3: Configure Your Project POM

### For Publishing Packages

Add distribution management to your `pom.xml`:

```xml
<project>
  <groupId>com.adonisjimenez</groupId>
  <artifactId>example-library</artifactId>
  <version>1.0.0</version>
  
  <distributionManagement>
    <repository>
      <id>github</id>
      <name>GitHub Packages</name>
      <url>https://maven.pkg.github.com/mr-adonis-jimenez/Python-Web-Scraper</url>
    </repository>
  </distributionManagement>
</project>
```

### For Consuming Packages

Add repository configuration to your `pom.xml`:

```xml
<project>
  <repositories>
    <repository>
      <id>github</id>
      <name>GitHub Packages</name>
      <url>https://maven.pkg.github.com/mr-adonis-jimenez/Python-Web-Scraper</url>
    </repository>
  </repositories>
  
  <dependencies>
    <dependency>
      <groupId>com.adonisjimenez</groupId>
      <artifactId>example-library</artifactId>
      <version>1.0.0</version>
    </dependency>
  </dependencies>
</project>
```

---

## 🚀 Step 4: Publish Package

### Deploy to GitHub Packages

```bash
mvn clean deploy
```

This command will:
1. Compile your project
2. Run tests
3. Package the artifact
4. Upload to GitHub Packages

### Verify Publication

Check your repository's Packages section:
```
https://github.com/mr-adonis-jimenez/Python-Web-Scraper/packages
```

---

## 📥 Step 5: Consume Package

In another project, add the dependency and run:

```bash
mvn clean install
```

Maven will automatically download the package from GitHub Packages.

---

## 👷 Step 6: GitHub Actions CI/CD (Optional)

### Auto-Publish on Release

Create `.github/workflows/publish-package.yml`:

```yaml
name: Publish Package to GitHub Packages

on:
  release:
    types: [created]
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: 'maven'
          server-id: github
          server-username: GITHUB_ACTOR
          server-password: GITHUB_TOKEN
      
      - name: Publish package
        run: mvn --batch-mode deploy -DskipTests
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📝 Complete Example POM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  
  <groupId>com.adonisjimenez</groupId>
  <artifactId>example-library</artifactId>
  <version>1.0.0</version>
  <packaging>jar</packaging>
  
  <name>Example Library</name>
  <description>Example library for GitHub Packages</description>
  
  <!-- Distribution Management for Publishing -->
  <distributionManagement>
    <repository>
      <id>github</id>
      <name>GitHub Packages</name>
      <url>https://maven.pkg.github.com/mr-adonis-jimenez/Python-Web-Scraper</url>
    </repository>
  </distributionManagement>
  
  <!-- Repository for Consuming -->
  <repositories>
    <repository>
      <id>github</id>
      <name>GitHub Packages</name>
      <url>https://maven.pkg.github.com/mr-adonis-jimenez/Python-Web-Scraper</url>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </repository>
  </repositories>
  
  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
  
  <dependencies>
    <!-- Your dependencies here -->
  </dependencies>
  
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
      </plugin>
    </plugins>
  </build>
</project>
```

---

## ✅ Verification Checklist

- [ ] Personal Access Token created with correct scopes
- [ ] `~/.m2/settings.xml` configured with GitHub credentials
- [ ] `pom.xml` has `distributionManagement` (for publishing)
- [ ] `pom.xml` has `repositories` (for consuming)
- [ ] Server `id` in settings.xml matches repository `id` in pom.xml
- [ ] Repository URL format: `https://maven.pkg.github.com/OWNER/REPOSITORY`
- [ ] Token stored securely (not in version control)

---

## 🔧 Troubleshooting

### Common Issues

**1. 401 Unauthorized**
```
Status: 401 Unauthorized
```
- Check token has correct scopes (`repo`, `write:packages`, `read:packages`)
- Verify token hasn't expired
- Confirm username and token in `settings.xml`

**2. 404 Not Found**
```
Return code is: 404, ReasonPhrase: Not Found
```
- Verify repository URL format
- Check repository exists and is accessible
- Ensure server ID matches between settings.xml and pom.xml

**3. Cannot Download Package**
- Check repository is public or you have access
- Verify `repositories` section in pom.xml
- Ensure authentication is configured

---

## 📚 Additional Resources

- [GitHub Packages Documentation](https://docs.github.com/en/packages)
- [Maven Settings Reference](https://maven.apache.org/settings.html)
- [GitHub Actions for Java](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-java-with-maven)

---

## 🔒 Security Best Practices

1. **Never commit tokens** to version control
2. **Use environment variables** for CI/CD
3. **Set token expiration** to minimize risk
4. **Rotate tokens regularly**
5. **Use minimal scopes** required for your use case
6. **Store tokens securely** (e.g., password manager)

---

## 🎯 Summary

**To Publish:**
```bash
# 1. Configure settings.xml with GitHub credentials
# 2. Add distributionManagement to pom.xml
# 3. Run:
mvn deploy
```

**To Consume:**
```bash
# 1. Configure settings.xml with GitHub credentials
# 2. Add repositories section to pom.xml
# 3. Add dependency
# 4. Run:
mvn install
```

---

**Created**: January 17, 2026  
**Token Generated**: `ghp_Fxwt1idJ1bf0rYqaiyqVQwnoJGG6sN3M6291`  
**Username**: `mr-adonis-jimenez`

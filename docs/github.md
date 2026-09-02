# GitHub 操作

本项目的 GitHub 认证统一使用本机环境变量 `GH_TOKEN`。真实 Token 不得写入仓库、`.env` 文件、脚本参数、日志或提交记录。

## Windows 配置

在 PowerShell 中持久化到当前用户环境：

```powershell
[Environment]::SetEnvironmentVariable('GH_TOKEN', '你的 GitHub Token', 'User')
```

重新打开终端后验证（只输出是否存在，不输出 Token）：

```powershell
if ([string]::IsNullOrWhiteSpace($env:GH_TOKEN)) { 'GH_TOKEN 未加载' } else { 'GH_TOKEN 已加载' }
```

GitHub CLI 会自动读取 `GH_TOKEN`，例如：

```powershell
gh auth status
gh repo create --source . --remote origin --push
```

若当前终端是在设置环境变量前打开的，请重新打开终端，或执行：

```powershell
$env:GH_TOKEN = [Environment]::GetEnvironmentVariable('GH_TOKEN', 'User')
```

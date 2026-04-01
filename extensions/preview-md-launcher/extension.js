const vscode = require('vscode');
const { execFile } = require('child_process');
const path = require('path');

const SCRIPT_PATH = path.join(
  process.env.HOME,
  '.claude',
  'skills',
  'preview-md',
  'scripts',
  'preview-md.mjs'
);

function getMarkdownFilePath(uri) {
  if (uri && uri.fsPath && uri.fsPath.endsWith('.md')) {
    return uri.fsPath;
  }
  const editor = vscode.window.activeTextEditor;
  if (editor && editor.document.languageId === 'markdown') {
    return editor.document.fileName;
  }
  return null;
}

function activate(context) {
  const disposable = vscode.commands.registerCommand(
    'previewMd.openInBrowser',
    (uri) => {
      const filePath = getMarkdownFilePath(uri);
      if (!filePath) {
        vscode.window.showWarningMessage('请打开一个 Markdown 文件');
        return;
      }

      const proc = execFile('node', [SCRIPT_PATH, filePath], (err) => {
        if (err) {
          vscode.window.showErrorMessage(`预览启动失败: ${err.message}`);
        }
      });

      proc.unref();
    }
  );

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };

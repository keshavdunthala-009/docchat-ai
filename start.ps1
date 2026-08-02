Write-Host 'Starting RAG Project...' -ForegroundColor Green
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd ''C:\Users\kesha\OneDrive\Attachments\Desktop - Copy\Desktop\RAG-PROJECT''; Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned; .\\venv\\Scripts\\Activate.ps1; cd backend; python main.py'
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd ''C:\Users\kesha\OneDrive\Attachments\Desktop - Copy\Desktop\RAG-PROJECT\\frontend''; npm run dev'
Write-Host 'Frontend: http://localhost:5173' -ForegroundColor Cyan
Write-Host 'Backend: http://localhost:8000' -ForegroundColor Cyan

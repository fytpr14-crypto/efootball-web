@echo off
cd /d "G:\pes\efootball-web"

git add .

git commit -m "update" 2>nul

git push

echo.
echo ✅ Deploy เสร็จแล้ว กดปิดหน้าต่างได้เลย
pause

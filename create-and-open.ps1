$shell = New-Object -ComObject Shell.Application
$folder = $shell.Windows() | Where-Object { $_.Name -like "*File Explorer*" -and $_.Visible } | Select-Object -First 1

$scriptFolder = $args[0].Trim('"')

Write-Host $scriptFolder
if ($null -ne $folder) {
    $path = $folder.Document.Folder.Self.Path
    $process = Start-Process -FilePath python -ArgumentList "$scriptFolder\main.py" -NoNewWindow -RedirectStandardOutput "$scriptFolder\output.txt" -PassThru

    Write-Host "Python PID: $($process.Id)"

    $process.WaitForExit()

    $name = Get-Content "$scriptFolder\output.txt"
    if($name -eq "None" -or $name -eq " "){
     Exit
    }
    else {
        if($name -ne ""){
             mkdir "$path\$name"
        }
        code "$path\$name"
        Exit
    }
}
Exit

$shell = New-Object -ComObject Shell.Application
$folder = $shell.Windows() | Where-Object { $_.Name -like "*File Explorer*" -and $_.Visible } | Select-Object -First 1 # selects the first visible File Explorer window

if($null -ne $folder){ # if no explorer found then the code exits 
    $path = $folder.Document.Folder.Self.Path
    $process = Start-Process -FilePath python -ArgumentList "D:/openWithVSCode/CreateAndOpen/main.py" -NoNewWindow -RedirectStandardOutput "D:/openWithVSCode/CreateAndOpen/output.txt" -PassThru

    Write-Host "Python PID: $($process.Id)"

    $process.WaitForExit() # Wait here after getting the process object

    $name = Get-Content "D:/openWithVSCode/CreateAndOpen/output.txt"
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


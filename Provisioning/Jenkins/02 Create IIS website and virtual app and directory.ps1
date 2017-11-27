Write-Output "Performing HTTPS bindings using Powershell"
$ipaddr = "172.30.9.19"
$port = 443
$sitename = "cliqtest"
$sslcert_subject = "WIN-*"

import-module webadministration | out-null
$bond_protocol = (Get-WebBinding -Port $port -Name $sitename).protocol
if ( $bond_protocol -ne "https") {
    Write-Output "Binding HTTPS to $ipaddr\:$port of $sitename"
    New-WebBinding -Name $sitename  -IPAddress $ipaddr -Port $port -Protocol https
} else {
    Write-Output "HTTPS has already bond to $ipaddr\:$port of $sitename"
}
Write-Output "Retrieving specified SSL certificate"
$SSLthumbprint = (Get-ChildItem Cert:\LocalMachine\My |? {$_.Subject -like "CN=$sslcert_subject"}| Select-Object -First 1).Thumbprint 
Write-Output "Binding HTTPS to IP $ipaddr\:$port of $sitename site with $SSLthumbprint of SSL certificate"
$SiteWithSSLcert=(Get-Item -Path IIS:\SslBindings\$ipaddr!$port -ErrorAction SilentlyContinue )
Write-Output "SiteWithSSLcert= $SiteWithSSLcert"
if ( $SiteWithSSLcert.Sites.Value -ne $sitename ) {
    Write-Output "Assigning $SSLthumbprint of SSL certificate to $sitename"
    Get-Item -Path "Cert:\LocalMachine\My\$SSLthumbprint" | new-item -Path IIS:\SslBindings\$ipaddr!$port -Force
} else {
    Write-Output "$sitename already has SSL certificate assigned"
}
Write-Output "Exiting Powershell for HTTPS binding"
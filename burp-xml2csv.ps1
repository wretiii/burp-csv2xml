param(
    [Parameter(Mandatory=$true)]
    [string]$i,
    [Parameter(Mandatory=$true)]
    [string]$o
)

function Clean-HTMLTags {
    param([string]$Text)
    if (-not $Text) { return $null }
    return $Text -replace '<[^>]+>', ''
}

# Load the XML file
$xml = [xml](Get-Content $i)

# Prepare data for CSV export
$csvData = foreach ($issue in $xml.issues.issue) {
    $host = Clean-HTMLTags $issue.host.InnerText
    $path = Clean-HTMLTags $issue.path.InnerText
    $fullPath = $host + $path
    [PSCustomObject]@{
        "Severity"                = Clean-HTMLTags $issue.severity.InnerText
        "Host"                    = $host
        "Path"                    = $path
        "Full Path"               = $fullPath
        "Issue Detail"            = Clean-HTMLTags $issue.issueDetail.InnerText
        "Name"                    = Clean-HTMLTags $issue.name.InnerText
        "Issue Background"        = Clean-HTMLTags $issue.issueBackground.InnerText
        "Remediation Background"  = Clean-HTMLTags $issue.remediationBackground.InnerText
    }
}

# Export to CSV, ensuring HTML tags are removed and using the inner text of XML elements
$csvData | Export-Csv -Path $o -NoTypeInformation

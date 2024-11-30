# OpenAI Models Listing Script

# Prompt for OpenAI API Key if not provided as argument
if (!$ApiKey) {
    $ApiKey = Read-Host "please enter openai api key"
}

# Set API Request Headers with Provided Key
$headers = @{
    "Authorization" = "Bearer $ApiKey"
}

# Invoke API Request to List Models
$response = Invoke-WebRequest -Uri "https://api.openai.com/v1/models" -Method Get -Headers $headers

# Check if the request was successful
if ($response.StatusCode -eq 200) {
    # Convert JSON response to a readable format and display
    $responseData = $response.Content | ConvertFrom-Json
    Write-Host "OpenAI Models Listing:"
    $responseData.data | Format-Table -Property id, object, created, owned_by
} else {
    Write-Host "Failed to retrieve models. Status Code:" $response.StatusCode
}
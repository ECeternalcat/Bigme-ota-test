# Bigme-ota-test
# OTA Capture Tool

This project is a Python-based tool designed to interact with an OTA (Over-The-Air) update server. It performs device registration and queries firmware updates using encrypted communication.

## Features

- **Device Registration**: Registers the device with the server by sending device-specific information.
- **Firmware Update Query**: Queries the server for available firmware updates.
- **RSA Encryption/Decryption**: Handles multi-block RSA encryption and decryption for secure communication.
- **Error Handling**: Provides clear error messages for decryption failures or network issues.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.7 or higher
- Required Python packages:
  - `requests`
  - `pycryptodomex` (for RSA encryption/decryption)

You can install the required packages using pip:

pip install requests pycryptodomex
Configuration
The script uses hardcoded values for device identification and server communication. These can be modified directly in the script:

SN: Device serial number
MODEL: Device model
V_NAME: Version name
PUB_HEX: Public RSA key in hexadecimal format
PRI_HEX: Private RSA key in hexadecimal format
Usage
To run the script, execute the following command:

python test.py
Steps Performed
Device Registration
The script sends a registration request to the server with the device's serial number, model, and version information.

## Firmware Update Query
After registration, the script queries the server for firmware updates. The request includes a timestamp and a unique identifier (xrz_none) for tracking purposes.

## Encryption and Decryption
All communication with the server is encrypted using RSA. The script handles both encryption of outgoing payloads and decryption of incoming responses.

## Known Issues

- **Firmware Download Link Not Returned**: Even with correct parameters, the server currently does not return a firmware download link. This may be due to server-side restrictions, such as recording the device's serial number or version history.

## Example Output
[*] Step 1: Performing device registration (Version: 3.0.6)...
    - Registration response: {"status": "success", "message": "Device registered"}

[*] Step 2: Checking firmware update (Probing version: 3.0.6)...

--- Firmware query decryption result ---
{"status": "success", "message": "No firmware update available"}
Note: In some cases, even though the server responds successfully, no firmware download link is returned due to validation failure.

## Error Handling
If an error occurs during decryption or communication, the script will output a descriptive message:

Decryption error: Incorrect padding
Request failed: 404
Security Notes
Ensure that the RSA keys (PUB_HEX and PRI_HEX) are kept secure and not exposed publicly.
Always validate server responses to prevent potential security vulnerabilities.

## License
This project is provided as-is without any warranty. Use at your own risk.

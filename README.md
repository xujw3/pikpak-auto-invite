# PikPak Auto Invitation

An automated tool for creating PikPak accounts and applying invitation codes.

## Features

- Automatically creates temporary email addresses using smailpro.com
- Handles captcha verification automatically
- Retrieves verification codes from emails
- Creates PikPak accounts with the provided invitation code
- Saves account information to JSON files
- Supports batch creation of multiple accounts

## Requirements

- Python 3.6+
- Required libraries:
  - Pillow
  - Requests
  - DrissionPage
  - colorama

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line:

```bash
python "PikPak Auto Invitation.py"
```

The script will:
1. Ask for the number of accounts you want to create
2. Ask for your invitation code (default: 123123123)
3. For each account:
   - Create a temporary email
   - Handle captcha verification
   - Retrieve the verification code from the email
   - Complete the registration process
   - Apply your invitation code
   - Save the account details to the ./account/ directory

## Configuration

You don't need to configure anything. The script handles everything automatically.

## Notes

- The created accounts will have a default password of "default123"
- Account information is saved in JSON format in the ./account/ directory
- The script includes a 5-second delay between account creations
- If you encounter any "too frequent" errors, the script will automatically retry

## Disclaimer

This tool is for educational and technical analysis purposes only. Please use responsibly and in accordance with PikPak's terms of service.

## Credits

Original developer: Please credit the source when sharing.

## License

Free to use for educational purposes.

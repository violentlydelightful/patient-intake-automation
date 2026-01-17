#!/usr/bin/env python3
"""
Patient Intake Automation System
Run this file to start the development server.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Patient Intake Automation System")
    print("=" * 50)
    print("\n  Starting server at: http://localhost:5100")
    print("  Press Ctrl+C to stop\n")
    app.run(debug=True, port=5100)

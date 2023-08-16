# Facial Recognition-based Attendance System with Voice Interaction

This project offers an innovative approach to automating the attendance process using facial recognition, enhanced with voice interactions for a seamless user experience. By integrating computer vision, voice recognition, and text-to-speech, the system ensures accuracy and adds a human touch to an otherwise automated process.

**Features:**

1. **Facial Recognition**:
   - **Directory Scanning**: The system scans a dedicated directory (`ImagesAttendance`) to load images of known individuals. These serve as the reference faces.
   - **Face Encoding**: Each reference image is processed to produce a unique set of numbers, or 'encodings', that identify the face.
   - **Real-time Recognition**: Leveraging the power of the OpenCV library and the specialized `face_recognition` library, the system continuously captures video frames, identifies faces, and matches them against the known encodings.

2. **Voice-Assisted New Face Registration**:
   - **Unknown Face Detection**: If the system encounters an unfamiliar face, it doesn't just display an 'Unknown' tag. Instead, it initiates a conversation.
   - **Voice Query**: The system verbally asks the new individual for their name using Google's Text-to-Speech API.
   - **Voice Recognition**: The person's response is captured and processed using the speech recognition library, extracting the spoken name.
   - **Visual & Voice Confirmation**: Once registered, the system provides a vocal acknowledgment, ensuring the person that their face has been stored for future reference.

3. **Attendance Logging**:
   - **Automated CSV Logging**: Recognized faces get their attendance marked in a CSV file, timestamped to the exact moment they were recognized.
   - **Error Correction**: If an error is made, the system has a mechanism to remove false attendance records.

4. **Interactive User Feedback**:
   - **Visual Indicators**: When faces are recognized, rectangles are drawn around them in the video feed. This gives visual feedback to users, ensuring they've been detected.
   - **Personalized Greetings**: Once a person has been in view for a while, the system greets them vocally by name, providing a friendly interaction.

5. **Scalability**:
   - The system can continually update its database of known faces. This makes it scalable for environments with changing populations, like schools with new students or companies with new employees.

**Technical Specifications**:

- **Languages & Libraries**:
  - Written in Python.
  - Uses OpenCV for video capture and basic image processing.
  - Employs the `face_recognition` library for facial detection and recognition.
  - Integrates `gTTS` (Google Text-to-Speech) for vocal interactions.
  - Uses the `speech_recognition` library for converting spoken words into text.

 **Imports**:
    - `gTTS`: Google Text-to-Speech API.
    - `os`: Interact with the operating system.
    - `speech_recognition`: Recognizes voice inputs.
    - `cv2`: OpenCV.
    - `numpy`: Handles numerical operations.
    - `face_recognition`: Recognizes and manipulates faces.
    - `datetime`: Fetches current date and time.

- **Platform Compatibility**:
  - Developed and tested on both macOS and Windows. Minor changes might be needed for full compatibility with other systems.

**Use Cases**:
- **Educational Institutions**: Automate attendance in classrooms, eliminating the need for manual roll calls.
- **Corporate Settings**: Track attendance in meetings or daily office check-ins.
- **Events & Conferences**: Swiftly register and check-in attendees without needing badges or manual entry.

---

In essence, this project blends the capabilities of modern AI tools to automate and enhance a routine task. The blend of facial recognition and voice interactivity not only simplifies attendance tracking but also makes it a more engaging experience.

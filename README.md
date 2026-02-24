# Cloud-Based-Automated-Parking-System
* This project presents a Cloud-orchestrated Automated Parking System built on Amazon Web Services (AWS) to enable automated and real-time parking operations.
* Vehicle entry/exit detection, slot allocation, billing, and SMS notifications are automated.
* The proposed solution improves parking efficiency, transparency, and user convenience.

## Core Technologies:
* Computer Vision (ANPR) for vehicle number plate detection.
* AWS Cloud Services for storage, processing, and notifications - accessed from AWS Management Console.
* Python-based code for automating slot allocation and billing.
<img width="1023" height="519" alt="image" src="https://github.com/user-attachments/assets/fb89b399-16c9-4c48-a395-af7fc036db75" /><br>AWS Management Console showing all cloud services


## System Architecture:
<img width="1404" height="935" alt="image" src="https://github.com/user-attachments/assets/9819814e-bbbb-4acb-844c-90c306a85f2c" />

### Architecture Focus:
* Seamless interaction between Camera System, Processing Engine, Cloud Database, and Notification Services.
* Centralized cloud-based control for scalability and reliability.

## Workflow of Proposed system
  
### Vehicle Detection & Recognition:
<img width="707" height="371" alt="image" src="https://github.com/user-attachments/assets/9af592fc-49c8-4bde-9a85-eeb733b35179" /><br>Sample vehicle image shown in front of camera.

<img width="975" height="530" alt="image" src="https://github.com/user-attachments/assets/2bca5311-d338-4e74-949e-220e09a4d8e8" /><br>Python Code is run from the terminal.
* Camera starts and captures vehicle image at parking entry.
* Image is uploaded to Amazon S3.
* * If detected vehicle number plate does not match with that of a parked vehicle, then entry is stored in DynamoDB.
* ANPR module processes the image to:
  * Detect number plate
  * Extract vehicle number using OCR
<img width="1746" height="624" alt="image" src="https://github.com/user-attachments/assets/1b559be1-88d5-4acd-97b6-053d6568e85a" /><br>Captured image stored in S3 bucket

### Slot Allocation Mechanism:
* Parking availability is fetched from DynamoDB (ParkingSlots table shown below).
* Nearest available slot is automatically assigned.
* Slot status is updated in real time (Available → Occupied).
<img width="1066" height="525" alt="image" src="https://github.com/user-attachments/assets/801430d3-93d6-4cc9-a8fe-9f317a9733a2" />

### Entry Logging:
* Vehicle entry details stored in ParkingEntries table shown in img below with parameters:
  * Vehicle Number
  * Slot ID
  * Entry Timestamp
<img width="1137" height="578" alt="image" src="https://github.com/user-attachments/assets/73ab3517-762f-422e-afd3-9f838687207d" />

### Billing & Exit Processing
<img width="707" height="371" alt="image" src="https://github.com/user-attachments/assets/9af592fc-49c8-4bde-9a85-eeb733b35179" /><br>Vehicle image shown in front of camera
<img width="1295" height="409" alt="image" src="https://github.com/user-attachments/assets/338e274d-4ad5-4f73-aea5-6f3e182da0c5" /><br>Python code is again run

* Camera starts and captures vehicle image.
* If detected vehicle number plate matches with that of a parked vehicle, then Parking Duration and bill calculated at its exit.
* Billing logic applied:
  * Flat ₹ 40 charged for first hour
  * Incremental charge per minute thereafter
* Bill amount generated automatically.

### Notification System
* SMS alert sent to user via AWS Simple Notification Service (SNS):
  * Entry confirmation and Slot details
  * Exit bill amount
 
<img width="464" height="955" alt="image" src="https://github.com/user-attachments/assets/c9832494-ceb0-46dd-b768-e25a18b0a500" /><br>SMS notifications informing: 
* slot to park the vehicle and time, when the vehicle enters
* total duration and bill amount to be paid when vehicle exits

## CONCLUSION

By combining real-time car recognition, automatic slot allocation, and cloud-based monitoring, the Cloud-Orchestrated Smart Parking Management System shows a notable improvement over conventional parking techniques.
By utilizing AWS cloud services and Automatic Number Plate Recognition (ANPR), the system enhances total parking space utilization, lowers waiting times, and offers high vehicle identification accuracy. The system's automation reduces human interaction, improves user convenience, and helps to lessen traffic jams and vehicle emissions in parking lots.
The results obtained from the system show that automation and cloud integration not only simplifies parking operations but also offer useful insights via data analytics, facilitating improved urban infrastructure management and planning.



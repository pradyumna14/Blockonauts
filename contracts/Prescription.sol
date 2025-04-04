// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Prescription {
    struct PrescriptionData {
        string doctorLicense;
        string patientName;
        uint256 patientAge;
        uint256 patientWeight;
        string medicalHistory;
        string patientID;
        string medicine;
        string dosage;
        uint256 tablets;
        string expiryDate;
        string datePrescribed;
        bool isDispensed;
    }

    mapping(string => PrescriptionData) private prescriptions;

    event PrescriptionStored(
        address indexed doctor, 
        string proof,
        string patientName,
        string medicine,
        string dosage,
        uint256 tablets,
        string expiryDate
    );

    event PrescriptionDispensed(string proof);

    /**
     * @dev Stores a new prescription and emits an event.
     */
    function storePrescription(string memory _proof, PrescriptionData memory _data) public {
        require(bytes(_proof).length > 0, "Invalid proof ID");
        require(bytes(prescriptions[_proof].patientID).length == 0, "Prescription already exists");
        require(bytes(_data.patientID).length > 0, "Invalid patient ID");

        _data.isDispensed = false;
        prescriptions[_proof] = _data;

        // 🔹 Emit event for pharmacists to retrieve from logs
        emit PrescriptionStored(
            msg.sender, 
            _proof,
            _data.patientName,
            _data.medicine,
            _data.dosage,
            _data.tablets,
            _data.expiryDate
        );
    }

    /**
     * @dev Retrieves a prescription.
     */
    function getPrescription(string memory _proof) public view returns (PrescriptionData memory) {
        require(bytes(prescriptions[_proof].patientID).length > 0, "Prescription not found");
        return prescriptions[_proof];
    }

    /**
     * @dev Marks a prescription as dispensed.
     */
    function dispensePrescription(string memory _proof) public {
        require(bytes(prescriptions[_proof].patientID).length > 0, "Prescription not found");
        require(!prescriptions[_proof].isDispensed, "Prescription already dispensed");

        prescriptions[_proof].isDispensed = true;
        emit PrescriptionDispensed(_proof);
    }
}
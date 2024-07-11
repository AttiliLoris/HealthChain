
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title HealthFiles
 * @dev This contract manages the creation and updates of health files.
 */
contract HealthFiles {
    // Struct to store health file information
    struct HealthFile {
        string cf;
        string clinicalHistory;
        string prescriptions;
        string treatmentPlan;
        string note;
    }

    // Mapping from cf to health file information
    mapping(string => HealthFile) public healthFiles;
    address public owner;
    event NewHealthFile(string indexed cf);
    event HealthFileUpdated(string indexed cf);
    event ConfirmTreatment(string indexed cfCaregiver, string indexed cfPatient);

    // Modifier to restrict access to the contract owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    // Constructor to set the contract deployer as the owner
    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Creates a new health file for a patient.
     * @param cf Codice fiscale (tax code) of the patient.
     * @param clinicalHistory Clinical history of the patient.
     * @param prescriptions List of prescriptions for the patient.
     * @param treatmentPlan List of treatment plans for the patient.
     * @param note List of notes for the patient.
     */
    //si può mettere i parametri di defualt a 0?
    function createHealthFile(string memory cf, string memory clinicalHistory, string memory prescriptions, string memory treatmentPlan, string memory note) public onlyOwner {
        require(bytes(healthFiles[cf].cf).length == 0, "Health file already exists");
        HealthFile memory newHealthFile = HealthFile(cf, clinicalHistory, prescriptions, treatmentPlan, note);
        healthFiles[cf] = newHealthFile;
        emit NewHealthFile(cf);
    }

     /**
     * @dev Updates a health file for a patient.
     * @param cf Codice fiscale (tax code) of the patient.
     * @param clinicalHistory Clinical history of the patient.
     * @param prescriptions List of prescriptions for the patient.
     * @param treatmentPlan List of treatment plans for the patient.
     * @param note List of notes for the patient.
     */
    function updateHealthFile(string memory cf, string memory clinicalHistory, string memory prescriptions, string memory treatmentPlan, string memory note) public onlyOwner {
        HealthFile storage healthFile = healthFiles[cf];
        healthFile.cf = cf;
        healthFile.clinicalHistory = clinicalHistory;
        healthFile.prescriptions = prescriptions;
        healthFile.treatmentPlan = treatmentPlan;
        healthFile.note = note;
        emit HealthFileUpdated(cf);
    }
     /**
     * @dev Gets the health file of a patient.
     * @param cf Codice fiscale (tax code) of the patient.
     * @return Clinical history, prescriptions, treatment plan, and notes of the patient.
     */
    function getHealthFile(string memory cf) public view returns (string memory clinicalHistory, string memory prescriptions, string memory treatmentPlan, string memory note) {
        HealthFile memory healthFile = healthFiles[cf];
        require(bytes(healthFile.cf).length != 0, "Health file not found");
        return (healthFile.clinicalHistory, healthFile.prescriptions, healthFile.treatmentPlan, healthFile.note);
    }

    function confirmTreatment(string memory cfCaregiver, string memory cfPatient) public  {
        emit ConfirmTreatment(cfCaregiver,cfPatient);
    }

}

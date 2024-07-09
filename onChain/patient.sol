// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Patients
 * @dev This contract manages the registration and updates of patient.
 */
contract Patients {
    // Struct to store patient information
    struct Patient {
        string name;
        string lastName;
        string birthday;
        string birthPlace;
        bool isRegistered;
        string cf;
    }

    // Mapping from cf to patient information
    mapping(string => Patient) public patients;
    mapping(address => bool) public authorizedEditors;
    address public owner;
    event PatientRegistered(string indexed cf, string indexed ctype);
    event PatientUpdated(string indexed cf, string indexed ctype);

    // Modifier to restrict access to the contract owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    //Restricts function access to either the contract owner or authorized editors.
    modifier onlyAuthorized() {
        require(msg.sender == owner || authorizedEditors[msg.sender], "Access denied: caller is not the owner or an authorized editor.");
        _;
    }

    // Constructor to set the contract deployer as the owner
    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Registers a new patient.
     * @param name First name of the patient.
     * @param lastName Last name of the patient.
     * @param birthday Birthday of the patient.
     * @param birthPlace Birth place of the patient.
     * @param cf Codice fiscale (tax code) of the patient.
     */
    function registerPatient(string memory name, string memory lastName, string memory birthday, string memory birthPlace, string memory cf) public onlyAuthorized{
        require(!patients[cf].isRegistered, "Patient already registered");
        patients[cf] = Patient(name, lastName, birthday, birthPlace, true, cf);
        emit PatientRegistered(cf, "patient");
    }

    /**
     * @dev Updates an existing patient's information.
     * @param name New first name of the patient.
     * @param lastName New last name of the patient.
     * @param birthday New birthday of the patient.
     * @param birthPlace New birth place of the patient.
     * @param cf New codice fiscale (tax code) of the patient.
     */
    function updatePatient(string memory name, string memory lastName, string memory birthday, string memory birthPlace, string memory cf) public onlyAuthorized{
        require(patients[cf].isRegistered, "Patient not found");
        Patient storage patient = patients[cf];
        patient.name = name;
        patient.lastName = lastName;
        patient.birthday = birthday;
        patient.birthPlace = birthPlace;
        patient.cf = cf;
        emit PatientUpdated(cf, "patient");
    }

     /**
     * @dev Gets the information of a registered patient.
     * @param cf Codice fiscale (tax code) of the patient.
     * @return name First name of the patient.
     * @return lastName Last name of the patient.
     * @return birthday Birthday of the patient.
     * @return birthPlace Birth place of the patient.
     * @return _cf Codice fiscale (tax code) of the patient.
     */
    function getPatient(string memory cf) public view returns (string memory name, string memory lastName, string memory birthday, string memory birthPlace, string memory _cf) {
        require(patients[cf].isRegistered, "Patient not found");
        Patient memory patient = patients[cf];
        return (patient.name, patient.lastName, patient.birthday, patient.birthPlace, patient.cf);
    }

}

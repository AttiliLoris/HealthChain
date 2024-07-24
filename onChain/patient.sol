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
        string birthPlace;
        string hashedPwd;
        bool isRegistered;
        bool isIndependent;
        string cf;
    }

    // Mapping from cf to patient information
    mapping(string => Patient) public patients;
    mapping(address => bool) public authorizedEditors;
    address public owner;
    event PatientRegistered(string cf, address indexed addres, string private_key, string ctype);
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
     * @param birthPlace Birth place of the patient.
     * @param cf Codice fiscale (tax code) of the patient.
     */
    function registerPatient(string memory name, string memory lastName, string memory birthPlace, string memory hashedPwd,bool isIndependent, string memory cf, address addres, string memory private_key)  public {
        require(!patients[cf].isRegistered, "Patient already registered");
        patients[cf] = Patient(name, lastName, birthPlace,hashedPwd,isIndependent, true, cf);
        emit PatientRegistered(cf,addres,private_key, "patient");
    }

    /**
     * @dev Updates an existing patient's information.
     * @param name New first name of the patient.
     * @param lastName New last name of the patient.
     * @param birthPlace New birth place of the patient.
     * @param cf New codice fiscale (tax code) of the patient.
     */
    function updatePatient(string memory name, string memory lastName, string memory birthPlace, string memory hashedPwd,bool isIndependent, string memory cf) public {
        require(patients[cf].isRegistered, "Patient not found");
        Patient storage patient = patients[cf];
        patient.name = name;
        patient.lastName = lastName;
        patient.birthPlace = birthPlace;
        patient.hashedPwd = hashedPwd;
        patient.isIndependent = isIndependent;
        patient.cf = cf;//cambio password come
        emit PatientUpdated(cf, "patient");
    }

     /**
     * @dev Gets the information of a registered patient.
     * @param cf Codice fiscale (tax code) of the patient.
     * @return name First name of the patient.
     * @return lastName Last name of the patient.
     * @return birthPlace Birth place of the patient.
     * @return hashedPwd password of the patient.
     * @return isIndependent of the patient.
     * @return _cf Codice fiscale (tax code) of the patient.
     */
    function getPatient(string memory cf) public view returns (string memory name, string memory lastName, string memory birthPlace, string memory hashedPwd,bool isIndependent, string memory _cf) {

        Patient memory patient = patients[cf];
        if (bytes(patient.cf).length == 0) {

                return ('', '', '', '', false, '');
        }
        return (patient.name, patient.lastName, patient.birthPlace,patient.hashedPwd,patient.isIndependent, patient.cf);
    }

}

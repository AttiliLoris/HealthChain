
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Doctors
 * @dev This contract manages the registration and updates of doctors.
 */
contract Doctors {
    // Struct to store doctor information
    struct Doctor {
        string name;
        string lastName;
        string hashedPwd;
        bool isRegistered;
        string cf;
    }

    // Mapping from cf to doctor information
    mapping(string => Doctor) public doctors;
    mapping(address => bool) public authorizedEditors;
    address public owner;
    event DoctorRegistered(string indexed cf, address indexed addres, string indexed private_key, string ctype);
    event DoctorUpdated(string indexed cf, string indexed ctype);

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
     * @dev Registers a new doctor.
     * @param name First name of the doctor.
     * @param lastName Last name of the doctor.
     * @param cf Codice fiscale (tax code) of the doctor.
     */

    function registerDoctor(string memory name, string memory lastName, string memory hashedPwd, string memory cf, address addres, string memory private_key) public onlyAuthorized{
        require(!doctors[cf].isRegistered, "Doctor already registered");
        doctors[cf] = Doctor(name, lastName, hashedPwd, true, cf);
        emit DoctorRegistered(cf,addres ,private_key ,"doctor");
    }

    /**
     * @dev Updates an existing doctor's information.
     * @param name New first name of the doctor.
     * @param lastName New last name of the doctor.
     * @param cf New codice fiscale (tax code) of the doctor.
     */
    function updateDoctor(string memory name, string memory lastName, string memory cf) public onlyAuthorized{
        require(doctors[cf].isRegistered, "Doctor not found");
        Doctor storage doctor = doctors[cf];
        doctor.name = name;
        doctor.lastName = lastName;
        doctor.cf = cf;
        emit DoctorUpdated(cf, "doctor");
    }
     /**
     * @dev Gets the information of a registered doctor.
     * @param cf Codice fiscale (tax code) of the doctor.
     * @return name First name of the doctor.
     * @return lastName Last name of the doctor.
     * @return hashedPwd password of the doctor.
     * @return _cf Codice fiscale (tax code) of the doctor.
     */
    function getDoctor(string memory cf) public view returns (string memory name, string memory lastName,string memory hashedPwd, string memory _cf) {
        Doctor memory doctor = doctors[cf];
         if (bytes(doctor.cf).length == 0) {
                return ("0", "0", "0", "0");
        }

        return (doctor.name, doctor.lastName, doctor.hashedPwd, doctor.cf);
    }
}

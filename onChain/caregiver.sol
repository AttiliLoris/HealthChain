
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Caregivers
 * @dev This contract manages the registration and updates of caregivers.
 */
contract Caregivers {
    // Struct to store caregiver information
    struct Caregiver {
        string name;
        string lastName;
        string hashedPwd;
        bool isRegistered;
        string cf;
    }

    // Mapping from cf to caregiver information
    mapping(string => Caregiver) public caregivers;
    mapping(address => bool) public authorizedEditors;
    address public owner;
    event CaregiverRegistered(string indexed cf, string indexed ctype);
    event CaregiverUpdated(string indexed cf, string indexed ctype);

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
     * @dev Registers a new caregiver.
     * @param name First name of the caregiver.
     * @param lastName Last name of the caregiver.
     * @param cf Codice fiscale (tax code) of the caregiver.
     */
    function registerCaregiver(string memory name, string memory lastName, string memory hashedPwd, string memory cf) public onlyAuthorized{
        require(!caregivers[cf].isRegistered, "Caregiver already registered");
        string memory hashedPassword = hashFunction(hashedPwd);
        caregivers[cf] = Caregiver(name, lastName,hashedPassword, true, cf);
        emit CaregiverRegistered(cf,"caregiver");
    }

    function hashFunction(string memory password) private pure returns (string memory) {
        return string(abi.encodePacked(keccak256(bytes(password))));
    }

    function verifyPassword(string memory cf, string memory password) public view returns (bool) {
        string memory hashedPassword = hashFunction(password);
        return keccak256(bytes(hashedPassword)) == keccak256(bytes(caregivers[cf].hashedPwd));
    }

    /**
     * @dev Updates an existing caregiver's information.
     * @param name New first name of the caregiver.
     * @param lastName New last name of the caregiver.
     * @param cf New codice fiscale (tax code) of the caregiver.
     */
    function updateCaregiver(string memory name, string memory lastName, string memory cf) public onlyAuthorized{
        require(caregivers[cf].isRegistered, "Caregiver not found");
        Caregiver storage caregiver = caregivers[cf];
        caregiver.name = name;
        caregiver.lastName = lastName;
        caregiver.cf = cf;
        emit CaregiverUpdated(cf, "caregiver");
    }
     /**
     * @dev Gets the information of a registered caregiver.
     * @param cf Codice fiscale (tax code) of the caregiver.
     * @return name First name of the caregiver.
     * @return lastName Last name of the caregiver.
     * @return hashedPwd password of the caregiver.
     * @return _cf Codice fiscale (tax code) of the caregiver.
     */
    function getCaregiver(string memory cf) public view returns (string memory name, string memory lastName,string memory hashedPwd, string memory _cf) {

        Caregiver memory caregiver = caregivers[cf];


        if (bytes(caregiver.cf).length == 0) {
                return ("0", "0", "0", "0");
        }
        return (caregiver.name, caregiver.lastName,caregiver.hashedPwd, caregiver.cf);
    }

}

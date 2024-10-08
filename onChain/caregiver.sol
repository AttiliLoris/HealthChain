
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
    event CaregiverRegistered(string  cf, address indexed addres, string  private_key, string ctype);
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
    function registerCaregiver(string memory name, string memory lastName, string memory hashedPwd, string memory cf, address addres, string memory private_key)  public onlyAuthorized{
        require(!caregivers[cf].isRegistered, "Caregiver already registered");
        caregivers[cf] = Caregiver(name, lastName,hashedPwd, true, cf);
        emit CaregiverRegistered(cf,addres,private_key,"caregiver");
    }

    /**
     * @dev Updates an existing caregiver's information.
     * @param name New first name of the caregiver.
     * @param lastName New last name of the caregiver.
     * @param cf New codice fiscale (tax code) of the caregiver.
     */
    function updateCaregiver(string memory name, string memory lastName, string memory cf) public {
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

from controller import mainController
from offChain.model.patient import Patient


def main():
    provider_url = "http://ganache:8080"
    patient_contracts = Patient(provider_url)

    # Sample data for testing
    private_key = "your_private_key"
    name = "John"
    lastname = "Doe"
    birthPlace = "City"
    pwd = "hashed_password"
    isIndependent = True
    cf = "0xYourAccountAddress"

    # Create a patient
    receipt = patient_contracts.create_patient(private_key, name, lastname, birthPlace, pwd, isIndependent, cf)
    print(f"Transaction receipt: {receipt}")

if __name__ == "__main__":
    main()
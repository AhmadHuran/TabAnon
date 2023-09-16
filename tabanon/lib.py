from cryptography.fernet import Fernet
import pandas as pd
from pathlib import Path

def reversible_anonymize_file(file_path, fields_to_anonymize, key=None, action="encrypt"):
    """
    Reversibly anonymizes the specified fields in the given file (CSV or XLSX).

    Args:
    - file_path (str): Path to the CSV or XLSX file.
    - fields_to_anonymize (list): List of columns to be anonymized.
    - key (bytes, optional): Encryption key. If not provided, a new key will be generated.
    - action (str): Either 'encrypt' or 'decrypt'.

    Returns:
    - DataFrame: Anonymized DataFrame.
    - bytes: Encryption key
    """

    if not key:
        key = Fernet.generate_key()
    cipher = Fernet(key)

    # Determine the file type
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, sep=";")
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please use CSV or XLSX.")

    # Encrypt or Decrypt the specified fields
    for field in fields_to_anonymize:
        if field == "": continue
        if field in df.columns:
            if action == "encrypt":
                df[field] = df[field].apply(lambda x: cipher.encrypt(str(x).encode()).decode('utf-8'))
            elif action == "decrypt":
                df[field] = df[field].apply(lambda x: cipher.decrypt(str(x).encode()).decode('utf-8'))
            else:
                raise ValueError("Invalid action. Use 'encrypt' or 'decrypt'.")
        else:
            raise ValueError(f"Field {field} not found in the file.")

    return df, key

def encrypt(file, info, key, output):
    with open(info, "r") as ff:
        data = ff.readlines()
    data = [ii.strip() for ii in data]
    df, key = reversible_anonymize_file(file, data, key=key, action="encrypt")

    file_path = Path(file)
    stem = file_path.stem
    suffix = f".enc.{file_path.suffix}"

    if not output is None:
        out_path = Path(output)
        output_prefix = out_path.parent / out_path.stem
        _suffix = out_path.suffix
        if _suffix in [".csv", ".xlsx"]:
            suffix = _suffix
        else:
            output_prefix = out_path

    info_out = f"{output_prefix}.enc.info"

    if suffix.endswith(".csv"):
        df.to_csv(f"{output_prefix}{suffix}", sep=";", index=False)
    else:
        df.to_excel(f"{output_prefix}{suffix}")
    with open(info_out, "w") as ff:
        for field in data:
            ff.write(field)
            ff.write("\n")
        ff.write(key.decode("utf-8"))

def decrypt(file, info, output):
    with open(info, "r") as ff:
        data = ff.readlines()
    data = [ii.strip() for ii in data]
    df, key = reversible_anonymize_file(file, data[:-1], key=data[-1], action="decrypt")

    file_path = Path(file)
    stem = file_path.stem
    suffix = file_path.suffix

    if not output is None:
        out_path = Path(output)
        output_prefix = out_path.parent / out_path.stem
        _suffix = out_path.suffix
        if _suffix in [".csv", ".xlsx"]:
            suffix = _suffix
        else:
            output_prefix = out_path

    info_out = f"{output_prefix}.dec.info"

    if suffix.endswith(".csv"):
        df.to_csv(f"{output_prefix}{suffix}", sep=";", index=False)
    else:
        df.to_excel(f"{output_prefix}{suffix}")

    with open(f"dec_{file}.info", "w") as ff:
        for field in data[:-1]:
            ff.write(field)
            ff.write("\n")

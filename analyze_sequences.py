# Store the FASTA file name.
filename = "Sequences.fasta"
# Import the CSV module to write results to a CSV file.
import csv

# Store the output file name.
output_file = "results.csv"

# Create a dictionary that maps DNA codons to amino acids.
codon_table = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G"
}

# Define a function to translate DNA into amino acids.
def translate_dna(dna):

    # Start with an empty amino acid sequence.
    amino_acids = ""

    # Read the DNA sequence three bases at a time.
    for i in range(0, len(dna) - 2, 3):

        # Extract one codon.
        codon = dna[i:i + 3]

        # Translate the codon into an amino acid.
        amino_acid = codon_table[codon]

        # Add the amino acid to the sequence.
        amino_acids = amino_acids + amino_acid

        # Stop translation when a stop codon is found.
        if amino_acid == "*":
            break

    # Return the translated sequence.
    return amino_acids

# Store the results for all sequences.
results = []
# Open the FASTA file and read it line by line.
with open(filename, "r") as file:

    # Start with an empty sequence ID.
    seq_id = ""

    # Start with an empty DNA sequence.
    dna = ""

    # Read each line in the file.
    for line in file:

        # Remove extra spaces and newline characters.
        line = line.strip()

        # Check if the line is a sequence ID.
        if line.startswith(">"):

            # Process the previous sequence if it exists.
            if seq_id != "":
                length = len(dna)
                gc_count = dna.count("G") + dna.count("C")
                gc_percent = (gc_count / length) * 100
                aa_sequence = translate_dna(dna)
                
                # Save the sequence information in the results list.
                results.append([seq_id, length, f"{gc_percent:.2f}", aa_sequence])

            # Save the new sequence ID.
            seq_id = line[1:]

            # Reset the DNA sequence.
            dna = ""

        # Otherwise, add the line to the DNA sequence.
        else:
            dna = dna + line

    # Process the last sequence.
    if seq_id != "":
        length = len(dna)
        gc_count = dna.count("G") + dna.count("C")
        gc_percent = (gc_count / length) * 100
        aa_sequence = translate_dna(dna)

        
        # Save the sequence information in the results list.
        results.append([seq_id, length, f"{gc_percent:.2f}", aa_sequence])
# Open the output CSV file for writing.
with open(output_file, "w", newline="") as file:

    # Create a CSV writer.
    writer = csv.writer(file)

    # Write the column names.
    writer.writerow(["id", "length", "gc_percent", "AA Sequence"])

    # Write all sequence results.
    writer.writerows(results)

# Print the table header.
print(f"{'id':<10}{'length':<10}{'gc_percent':<15}{'AA Sequence'}")

# Print a separator line.
print("-" * 60)

# Print each sequence result.
for row in results:
    print(f"{row[0]:<10}{row[1]:<10}{row[2] + '%':<15}{row[3]}")

# Print a separator line.
print("-" * 60)

# Print a confirmation message.
print(f"Saved {len(results)} records to {output_file}.")

package main

import (
	"encoding/hex"
	"encoding/json"
	"golang.org/x/crypto/nacl/secretbox"
	"os"
)

type Input struct {
	Problem1 []int    `json:"problem1"`
	Problem2 string   `json:"problem2"`
	Problem3 string   `json:"problem3"`
	Problem4 string   `json:"problem4"`
	Problem5 []string `json:"problem5"`
}

type Output struct {
	Problem1 struct {
		Sum     int `json:"sum"`
		Product int `json:"product"`
	} `json:"problem1"`
	Problem2 string `json:"problem2"`
	Problem3 string `json:"problem3"`
	Problem4 string `json:"problem4"`
	Problem5 string `json:"problem5"`
}

func main() {
	var input Input
	var output Output
	err := json.NewDecoder(os.Stdin).Decode(&input)
	if err != nil {
		panic(err)
	}

	// Problem 1
	output.Problem1.Sum = 0
	output.Problem1.Product = 1
	for i := 0; i < len(input.Problem1); i++ {
		output.Problem1.Sum += input.Problem1[i]
		output.Problem1.Product *= input.Problem1[i]
	}

	// Problem 2
	decoded, err := hex.DecodeString(input.Problem2)
	if err != nil {
		panic(err)
	}
	output.Problem2 = string(decoded)

	// Problem 3
	output.Problem3 = hex.EncodeToString([]byte(input.Problem3))

	// Problem 4
	key := [32]byte{}
	for i := 0; i < 32; i++ {
		key[i] = 'A'
	}
	nonce := [24]byte{}
	for i := 0; i < 24; i++ {
		nonce[i] = 'B'
	}
	ciphertext, err := hex.DecodeString(input.Problem4)
	if err != nil {
		panic(err)
	}
	plaintext, isValid := secretbox.Open(nil, ciphertext, &nonce, &key)
	if !isValid {
		panic("ciphertext invalid")
	}
	output.Problem4 = string(plaintext)

	// Problem 5
	for i := 0; i < 32; i++ {
		key[i] = 'C'
	}
	for i := 0; i < 24; i++ {
		nonce[i] = 'D'
	}
	for i := 0; i < len(input.Problem5); i++ {
		ciphertext, err := hex.DecodeString(input.Problem5[i])
		if err != nil {
			panic(err)
		}
		plaintext, isValid := secretbox.Open(nil, ciphertext, &nonce, &key)
		if isValid {
			output.Problem5 = string(plaintext)
			break
		}
	}

	// Output
	encoder := json.NewEncoder(os.Stdout)
	// pretty printing
	encoder.SetIndent("", "  ")
	err = encoder.Encode(&output)
	if err != nil {
		panic(err)
	}
}

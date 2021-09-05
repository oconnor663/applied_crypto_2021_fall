package solution;

import com.google.common.io.BaseEncoding;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.goterl.lazysodium.LazySodiumJava;
import com.goterl.lazysodium.SodiumJava;
import com.goterl.lazysodium.exceptions.SodiumException;
import com.goterl.lazysodium.utils.Key;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class App {
  static class Inputs {
    ArrayList<Integer> problem1;
    String problem2;
    String problem3;
    String problem4;
    ArrayList<String> problem5;
  }

  static class Outputs {
    Problem1Output problem1;
    String problem2;
    String problem3;
    String problem4;
    String problem5;
  }

  static class Problem1Output {
    int sum;
    int product;
  }

  public static void main(String[] args) throws Exception {
    Gson gson = new GsonBuilder().setPrettyPrinting().create();
    Inputs inputs = gson.fromJson(new InputStreamReader(System.in), Inputs.class);
    Outputs outputs = new Outputs();

    // Problem 1
    outputs.problem1 = new Problem1Output();
    outputs.problem1.sum = 0;
    outputs.problem1.product = 1;
    for (int x : inputs.problem1) {
      outputs.problem1.sum += x;
      outputs.problem1.product *= x;
    }

    // Problem 2
    byte[] output_bytes = BaseEncoding.base16().lowerCase().decode(inputs.problem2);
    outputs.problem2 = new String(output_bytes);

    // Problem 3
    outputs.problem3 = BaseEncoding.base16().lowerCase().encode(inputs.problem3.getBytes());

    // Problem 4
    LazySodiumJava sodium = new LazySodiumJava(new SodiumJava());
    Key key4 = Key.fromPlainString("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
    byte[] nonce4 = "BBBBBBBBBBBBBBBBBBBBBBBB".getBytes();
    // Note that this overload of cryptoSecretBoxOpenEasy does hex encoding internally.
    outputs.problem4 = sodium.cryptoSecretBoxOpenEasy(inputs.problem4, nonce4, key4);

    // Problem 5
    Key key5 = Key.fromPlainString("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC");
    byte[] nonce5 = "DDDDDDDDDDDDDDDDDDDDDDDD".getBytes();
    for (String ciphertext : inputs.problem5) {
      try {
        // Note that this overload of cryptoSecretBoxOpenEasy does hex encoding internally.
        outputs.problem5 = sodium.cryptoSecretBoxOpenEasy(ciphertext, nonce5, key5);
        break;
      } catch (SodiumException e) {
        continue;
      }
    }

    gson.toJson(outputs, System.out);
    System.out.println();
  }
}

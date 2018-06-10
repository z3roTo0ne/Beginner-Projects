package com.example.java;

import java.io.*;
import java.net.*;
import java.util.Arrays;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Scanner;

public class File_Share {
    public static void main(String args[]) throws Exception {
        Scanner reader = new Scanner(System.in);
        System.out.print("Do you want to connect or listen for an incoming connection? (C/L): ");
        String answer = reader.next();

        reader = new Scanner(System.in);
        System.out.print("Where do you want to save file (Enter a path): ");
        String path = reader.nextLine();

        if(answer.equals("L") || answer.equals("l")){
            reader = new Scanner(System.in);
            System.out.print("Enter port you want to listen on: ");
            int port = reader.nextInt();

            listen(port, path);
        }
        else if(answer.equals("C") || answer.equals("c")){
            reader = new Scanner(System.in);
            System.out.print("Enter host IP you want to connect to: ");
            String host = reader.next();

            reader = new Scanner(System.in);
            System.out.print("Enter port you want to connect to: ");
            int port = reader.nextInt();

            connect(host, port, path);
        }
        else {
            System.out.println("Wrong input please try again");
        }
    }

    private  static void listen(int port, final String save_path) throws IOException {
        System.out.println("Creating Socket 1");
        ServerSocket ss = new ServerSocket(port);

        System.out.println("Accepting incoming requests");
        Socket s = ss.accept();

        // Needed to connect message to client
        System.out.println("Creating output stream");
        OutputStream socketoutstr = s.getOutputStream();
        OutputStreamWriter osr = new OutputStreamWriter( socketoutstr );
        final BufferedWriter bw = new BufferedWriter( osr );

        // Needed to receive a message from client
        System.out.println("Creating input stream");
        InputStream socketinstr = s.getInputStream();
        InputStreamReader isr = new InputStreamReader( socketinstr );
        final BufferedReader br = new BufferedReader( isr );

        System.out.println("Connected\n");
        System.out.print("Enter Path to file you want to send: ");


        Thread thread1 = new Thread(){
            public void run(){
                while(true) {
                    try {
                        send(bw);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        };

        Thread thread2 = new Thread(){
            public void run(){
                while(true){
                    try {
                        receive(br, save_path);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        };

        thread1.start();
        thread2.start();
    }

    private static void connect(String host, int port, final String save_path) throws IOException {
        // Create socket (will automatically connect)
        System.out.println("Creating Socket 1");
        Socket s = new Socket(host, port);

        // Needed to connect message to server
        System.out.println("Creating output stream");
        OutputStream socketoutstr = s.getOutputStream();
        final OutputStreamWriter osr = new OutputStreamWriter( socketoutstr );
        final BufferedWriter bw = new BufferedWriter( osr );

        // Needed to receive a message from server
        System.out.println("Creating input stream");
        InputStream socketinstr = s.getInputStream();
        InputStreamReader isr = new InputStreamReader( socketinstr );
        final BufferedReader br = new BufferedReader( isr );

        System.out.println("Connected\n");
        System.out.print("Enter Path to file you want to send and press enter: ");

        Thread thread1 = new Thread(){
            public void run(){
                while(true) {
                    try {
                        send(bw);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        };

        Thread thread2 = new Thread(){
            public void run(){
                while(true){
                    try {
                        receive(br, save_path);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        };

        thread1.start();
        thread2.start();
    }

    private static void send(BufferedWriter bw) throws IOException {
        // Code to get User Input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String path = null;
        String file_extension = null;
        String file_name = null;
        try {
            path = br.readLine();
        } catch (IOException e) {
            e.printStackTrace();
        }

        String arrayString = file_to_String(path);

        // Print User Input
        System.out.println("Sending File: " + path);

        try {
            file_extension = path.split("\\.")[1];
        }
        catch (IndexOutOfBoundsException e){

        }

        try{
            file_name = string_between_two_chars(path, '/', '.');
        }
        catch (NullPointerException e){

        }

        // Send User Input
        try {
            if(file_name != null) {
                bw.write(file_name + '.' + file_extension + arrayString);
            }
            else {
                bw.write(arrayString);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            bw.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            bw.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("Sent File: " + path + '\n');
        System.out.print("Enter Path to file you want to send and press enter: ");
    }

    private static void receive(BufferedReader br, String save_path) throws IOException {

        String file_extension;
        String file_name;

        // Read Received Message
        String received = null;
        try {
            received = br.readLine();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Print Received Message if it is not null
        if(received != null && received.contains("[")) {
            String received_mod = received.substring(received.indexOf("["));
            System.out.println("\nReceived File" + "\n");
            System.out.print("Enter Path to file you want to send and press enter: ");
            String extract = received.substring(0, Math.min(received.length(), 40));
            String extract2 = extract.split("\\[")[0];
            file_name = extract2.split("\\.")[0];
            file_extension = extract2.split("\\.")[1];
            save_path = (save_path + "/" + file_name + "." + file_extension).replace("//", "/");

            string_to_file(received_mod, save_path);

        }
    }


    private static void close(BufferedWriter bw, BufferedReader br, Socket s, ServerSocket ss) throws IOException {
        bw.close();
        br.close();
        s.close();
        ss.close();
    }

    private static byte[] readBytes(InputStream inputStream) throws IOException {
        byte[] b = new byte[1024];
        ByteArrayOutputStream os = new ByteArrayOutputStream();
        int c;
        while ((c = inputStream.read(b)) != -1) {
            os.write(b, 0, c);
        }
        return os.toByteArray();
    }

    private static void writeBytesToFile(byte[] bFile, String fileDest) {
        FileOutputStream fileOutputStream = null;

        try {
            fileOutputStream = new FileOutputStream(fileDest);
            fileOutputStream.write(bFile);

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (fileOutputStream != null) {
                try {
                    fileOutputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }


    private static String string_between_two_chars(String s, char c1, char c2){
        s = s.substring(s.lastIndexOf(c1) + 1);
        s = s.substring(0, s.indexOf(c2));
        return s;
    }

    private static String file_to_String(String file_path) throws IOException {
        String file_string;
        byte[] array = readBytes(new FileInputStream(file_path));
        file_string = Arrays.toString(array);
        return file_string;
    }

    private static void string_to_file(String file_string, String save_path){
        String[] byteValues = file_string.substring(1, file_string.length() - 1).split(",");

        byte[] arrayStringtoByte = new byte[byteValues.length];
        for (int i=0, len=arrayStringtoByte.length; i<len; i++) {
            arrayStringtoByte[i] = Byte.parseByte(byteValues[i].trim());
        }
        writeBytesToFile(arrayStringtoByte, save_path);

    }

}

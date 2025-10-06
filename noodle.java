import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Where's my LAMB SAUCE");
            return;
        }

        String fileName = args[0];
        String outputName = args[1];
        System.out.println("LAMB SAUCE is in a pot");

        BufferedImage src  = null;
        try {
            src = ImageIO.read(new File(fileName));
        } catch (IOException e) {
            System.out.println("This isn't LAMB SAUCE");
        }

        int width = src.getWidth();
        int height = src.getHeight();

        byte[][] input = new byte[width+2][height+2];
        byte[][] output = new byte[width+2][height+2];

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int gray = src.getRGB(x, y) & 0xFF; // directly use lower 8 bits
                input[y + 1][x + 1] = (byte) gray;
            }
        }

        for (int i=0; i<width; i++) {
            for (int j=1; j<height; j++) {
                int oldVal = Byte.toUnsignedInt(input[i][j]);
                int newVal = (oldVal < 128) ? 0 : 255;
                output[i][j] = (byte) (newVal == 0 ? 0 : 1);
                int err = oldVal - newVal;

//                input[i][j + 1]     = clamp(Byte.toUnsignedInt(input[i][j + 1])     + (err * 7) / 16);
//                input[i + 1][j - 1] = clamp(Byte.toUnsignedInt(input[i + 1][j - 1]) + (err * 3) / 16);
//                input[i + 1][j]     = clamp(Byte.toUnsignedInt(input[i + 1][j])     + (err * 5) / 16);
//                input[i + 1][j + 1] = clamp(Byte.toUnsignedInt(input[i + 1][j + 1]) + (err * 1) / 16);

                input[i][j+1] += (err*7)/16;
                input[i+1][j-1] += (err*3)/16;
                input[i+1][j] += (err*5)/16;
                input[i+1][j+1] += (err*1)/16;
            }
        }

        BufferedImage outImg = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_BINARY);
        for (int y = 1; y <= height; y++) {
            for (int x = 1; x <= width; x++) {
                int val = (output[y][x] == 0) ? 0x000000 : 0xFFFFFF;
                outImg.setRGB(x - 1, y - 1, val);
            }
        }


        try {
            ImageIO.write(outImg, "png", new File(outputName));
        } catch (IOException e) {
            System.out.println("palce");
        }
        System.out.println("✅ Done! " + outputName);
    }

    private static byte clamp(int v) {
        if (v < 0) v = 0;
        if (v > 255) v = 255;
        return (byte) v;
    }
}

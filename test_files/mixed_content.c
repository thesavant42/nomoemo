/* Test File 4: Mixed Content (C-style comments)
 * This file contains emojis in a different file format
 * to test cross-language emoji detection
 */

#include <stdio.h>
#include <stdlib.h>

// Function with emoji in comment
int calculate_area(int width, int height) {
    // Calculate area of rectangle ⚙️
    printf("Calculating area...\n");  // Gear emoji in comment
    return width * height;
}

// Status reporting function
void report_status(int code) {
    switch(code) {
        case 0:
            printf("Success ✅\n");  // Success checkmark
            break;
        case 1:
            printf("Warning ⚠️\n");  // Warning triangle
            break;
        case 2:
            printf("Error ❌\n");    // Red X mark
            break;
        default:
            printf("Unknown status ❓\n");  // Question mark
    }
}

// Main function
int main() {
    printf("Starting application... 🚀\n");  // Rocket emoji
    
    int area = calculate_area(10, 20);
    printf("Area: %d square units 🟦\n", area);  // Square emoji
    
    report_status(0);  // Report success
    
    printf("Application completed! 🎉\n");  // Party popper emoji
    return 0;
}
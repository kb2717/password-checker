#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <time.h>

#define MAX_LEN 100

// ANSI color codes
#define RED "\033[1;31m"
#define YELLOW "\033[1;33m"
#define GREEN "\033[1;32m"
#define RESET "\033[0m"

// Function to calculate password strength (0–100)
int getStrength(const char *pass) {
    int len = strlen(pass);
    int lower = 0, upper = 0, digit = 0, special = 0;

    for (int i = 0; i < len; i++) {
        if (islower(pass[i])) lower = 1;
        else if (isupper(pass[i])) upper = 1;
        else if (isdigit(pass[i])) digit = 1;
        else special = 1;
    }

    int score = (lower + upper + digit + special) * 20;
    score += (len >= 8) ? 20 : len * 2.5;

    for (int i = 0; i < len - 1; i++)
        if (pass[i] == pass[i + 1]) score -= 5;

    if (score > 100) score = 100;
    if (score < 0) score = 0;
    return score;
}

// Generate a stronger password (at least 8 characters)
void makeStrongPassword(char *newPass, int len) {
    if (len < 8) len = 8;  // Ensure minimum length = 8

    char lower[] = "abcdefghijklmnopqrstuvwxyz";
    char upper[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    char digits[] = "0123456789";
    char special[] = "!@#$%^&*()-_=+<>?";
    char all[200];
    sprintf(all, "%s%s%s%s", lower, upper, digits, special);
    int total = strlen(all);

    srand(time(NULL));

    // Ensure at least one of each type
    if (len > 0) newPass[0] = lower[rand() % 26];
    if (len > 1) newPass[1] = upper[rand() % 26];
    if (len > 2) newPass[2] = digits[rand() % 10];
    if (len > 3) newPass[3] = special[rand() % strlen(special)];

    // Fill the remaining characters randomly
    for (int i = 4; i < len; i++)
        newPass[i] = all[rand() % total];

    // Shuffle characters for randomness
    for (int i = 0; i < len; i++) {
        int j = rand() % len;
        char temp = newPass[i];
        newPass[i] = newPass[j];
        newPass[j] = temp;
    }

    newPass[len] = '\0';
}

// Display color-coded strength
void printStrengthColor(int strength) {
    if (strength < 40)
        printf(RED "Weak (%d%%)\n" RESET, strength);
    else if (strength < 80)
        printf(YELLOW "Moderate (%d%%)\n" RESET, strength);
    else
        printf(GREEN "Strong (%d%%)\n" RESET, strength);
}

int main() {
    char password[MAX_LEN], newPass[MAX_LEN];

    printf("Enter your password: ");
    fgets(password, MAX_LEN, stdin);
    password[strcspn(password, "\n")] = 0;

    int strength = getStrength(password);
    printf("\nYour Password: %s\nStrength: ", password);
    printStrengthColor(strength);

    if (strength < 80) {
        int newLen = strlen(password);
        if (newLen < 8) newLen = 8;  // Adjust to minimum 8 chars

        makeStrongPassword(newPass, newLen);
        int newStrength = getStrength(newPass);
        printf("\nSuggested Stronger Password: %s\nStrength: ", newPass);
        printStrengthColor(newStrength);
    } else {
        printf("\nYour password is strong enough!\n");
    }

    return 0;
}

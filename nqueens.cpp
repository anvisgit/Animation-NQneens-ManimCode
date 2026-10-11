
#include <iostream>
#include <chrono>
using namespace std;

int board[20];
bool col[20], diag1[40], diag2[40];
long long solutions = 0, calls = 0;
int n;

void solve(int row) {
    calls++;

    if (row == n) {
        solutions++;
        cout << "\nSolution " << solutions << ":\n";
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++)
                cout << (board[i] == j ? "Q " : ". ");
            cout << "\n";
        }
        return;
    }

    for (int c = 0; c < n; c++) {
        int d1 = row - c + n - 1;
        int d2 = row + c;

        if (!col[c] && !diag1[d1] && !diag2[d2]) {
            board[row] = c;
            col[c] = diag1[d1] = diag2[d2] = true;

            solve(row + 1);

            col[c] = diag1[d1] = diag2[d2] = false;
        }
    }
}

int main() {
    cout << "Enter N (1-20): ";
    cin >> n;

    if (n < 1 || n > 20) {
        cout << "Invalid N\n";
        return 0;
    }

    auto start = chrono::high_resolution_clock::now();

    solve(0);

    auto end = chrono::high_resolution_clock::now();
    double ms = chrono::duration<double, milli>(end - start).count();

    cout << "\nTotal solutions: " << solutions;
    cout << "\nRecursive calls: " << calls;
    cout << "\nExecution time: " << ms << " ms\n";

    return 0;
}

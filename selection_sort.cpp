class Solution {
    public:
        vector<int> selectionSort(vector<int>& nums) {
            int n = nums.size();
            for (int i = 0; i <= n - 2; i++) {
                int mini = i;
                for (int j = i; j <= n - 1; j++) {
                    if (nums[j] < nums[mini]) {
                        mini = j;
                    }
                }
                swap(nums[i], nums[mini]);
            }
            return nums;
        }
    };
    
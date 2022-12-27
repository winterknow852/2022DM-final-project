# DM final project_MDL

* 實驗環境：python 3.7
* 資料集來源：paper範例 & 作業1資料集

* 變數說明：
:::info
1. **itemset_data** : standard code table itemset
2. **ST_codeword** : dict of standard code table's codeword and usage
3. **Ntrivial_codeword_** : non-trivial code table's codeword
4. **Ntrivial_usage** : dict of non-trivial code table's codeword and usage 
5. **Ntrivial_encode** : data encoded with non-trivial code table
:::

* 程式碼運行方式：
1. 讀入csv形式的dataset
2. 將資料及轉成binary的形式以方便後續的資料運用
3. 計數dataset內每一個item的數量
4. 建立standard code table，用來encoded資料集
5. 建立non-trivial code table，並且用它來encoded資料集
6. 定義2個function non_trivialCT 以及 data_encode 分別用來處理建立non-trivial code table 以及 encoded
    * **non_trivialCT**：從第一個transaction開始找長度最長的itemset作為codeword，並檢查該codeword在整個dataset出現的次數，若是只有一次，就不可以做為codeword，就往下從下一筆transaction找codeword。
    ```python=
     def non_trivialCT(data_binary,item):
        codeword = []
        in_codeword = np.zeros(len(itemset)) #whether the item is used 
        ......
        return return codeword
    ```
    * **data_encode**：用上一步建立的codeword來encoded data，同時計算每一個codeword的usage。
     ```python=
      def data_encode(data_encode,codeword):
        usage = []
        encode_CT = {}
        ......
        return code_usage,encode_CT
     ```
7. 定義3個function：Lst、Lct以及LDM來計算description length
    * Lst 計算itemset的長度
    ```python=
    def Lst(itemset,data_itemset):
        lst = 0
        ......
        return lst
    ```
    * Lct 計算 codeword的長度
    ```python=
    def Lct(itemset,data_itemset):
        lct = 0
        ......
        return lct
    ```
    * LDM 計算 encoded後data的長度(itemsets occurrences)
    ```python=
    def LDM(itemset,data_itemset):
        ldm = 0
        ......
        return ldm
    ```
8. 最後把Lst、Lct以及LDM計算出來的結果加總起來，就是最後總長度

 


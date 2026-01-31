<script setup>
import { mainWallet, customWallet, Username, isLoggedIn, MAIN_WALLET_ID, CUS_WALLET_ID } from '@/constants';
import { onMounted, ref } from 'vue';
import { Icon } from "@iconify/vue";
import api from '@/api';
import { transactions, budgets, goals } from '@/sharedStates';


defineProps({ //passed props
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    required: true
  },
  headersArr: {
    type: Array,
    required: true
  },
  isGoalsTable: {
    type: Boolean,
    default: false
  },
  isTransTable: {
    type: Boolean,
    default: false
  },
  isBudgetTable: {
    type: Boolean,
    default: false
  }
});

const user = localStorage.getItem(Username)
const isLogged = localStorage.getItem(isLoggedIn)

let mainWalletName = ""
let customWalletName = ""

const mainWalletData = JSON.parse(localStorage.getItem(`${mainWallet}_${user}`));
const customWalletData = JSON.parse(localStorage.getItem(`${customWallet}_${user}`));

if(mainWalletData) {
  mainWalletName = mainWalletData.formName;
}

if(customWalletData) {
  customWalletName = customWalletData.formName;
}



const amount = ref("")
const currAmount = ref("")
const targetAmount = ref("")
const desc = ref("")
const date = ref("")
const targetDate = ref("")
const category = ref("")
const transType = ref("")
const wallet = ref("")

const error = ref("")

const goalUpdate = ref("")

const sanitizeNums= () => { //sanitizes number input e.g. amount of money
  amount.value = amount.value.replace(/[^0-9]/g, '')
  currAmount.value = currAmount.value.replace(/[^0-9]/g, '')
  targetAmount.value = targetAmount.value.replace(/[^0-9]/g, '')
  goalUpdate.value = goalUpdate.value.replace(/[^0-9]/g, '')
}

const sanitizeDesc= () => { //sanitizes describtion text 
   desc.value = desc.value.replace(/[<>\/\\{}\[\]]/g, '')
}



const getRecordData = async (url, arr) => { //fetching record data for transactions, budgets, and goals tables
try {
    const res = await api.get(`${url}/`);

    if(res.status === 200) {
      arr.value = res.data
    } else {
      console.log(`error fetching tables`)
    }
    } catch(e) {
      console.error(`fetching ${arr} error:`, e)
    }
}



const handleBudgCreate = async () => {
if(!amount.value || !desc.value || !date.value || !category.value ) {
    error.value = "Please Fill In All Fields"
    return;
  } else {
    error.value = ""
    if(isLogged && user) {
    try {
    const res = await api.post('budget/', { //posting transaction to backend
      category: category.value,
      amount: amount.value,
      budg_date: date.value,
      desc: desc.value
    });

    if(res.status=== 201) {
      await getRecordData('budget', budgets)
      
      
    } else {
      alert("posting budget failed")
    }
    
  } catch(e) {
      console.error('posting budget error:', e)
    }
  }
  amount.value = ""
  desc.value = ""  
  date.value = ""
  category.value = ""
}
}


const handleGoalCreate = async () => {
if(!currAmount.value || !desc.value || !date.value || !category.value || !targetAmount.value || !targetDate.value) {
    error.value = "Please Fill In All Fields"
    return;
  } else {
    error.value = ""
    if(isLogged && user) {
    try {
    const res = await api.post('goal/', { //posting goal record to backend
        target_amount: targetAmount.value,
        current_amount: currAmount.value,
        category: category.value,
        start_date: date.value,
        target_date: targetDate.value,
        desc: desc.value
    });

    if(res.status=== 201) {
      await getRecordData('goal', goals)
      
    } else {
      alert("posting goal failed")
    }
    
  } catch(e) {
      console.error('posting goal error:', e)
    }
  }
  currAmount.value = ""
  desc.value = ""  
  date.value = ""
  category.value = ""
  targetAmount.value = ""
  targetDate.value = ""
}
}


const handleTransCreate = async () => {
  const main_w_id = localStorage.getItem(`${MAIN_WALLET_ID}_${user}`)
  const custom_w_id = localStorage.getItem(`${CUS_WALLET_ID}_${user}`)
  if(!amount.value || !desc.value || !date.value || !category.value || !transType.value || !wallet.value) {
    error.value = "Please Fill In All Fields"
    return;
  } 
    error.value = ""
    if(isLogged && user) {
    try {
    const res = await api.post('trans/', { //posting transaction to backend
      wallet: wallet.value === 'Main' ? main_w_id : custom_w_id,
      trans_type: transType.value,
      amount: amount.value,
      trans_date: date.value,
      category: category.value,
      desc: desc.value
    });

    if(res.status === 201) {
      await getRecordData('trans', transactions)

      if(wallet.value === "Main") { //updating locally stored wallet values depending on the transaction type (income or expense)
        const mainWalletData = JSON.parse(localStorage.getItem(`${mainWallet}_${user}`)) || { formName: "", formValue: 0 };
          if (transType.value === 'Income') {
            mainWalletData.formValue += Number(amount.value);
          } else {
            mainWalletData.formValue -= Number(amount.value);
          }
        localStorage.setItem(`${mainWallet}_${user}`, JSON.stringify(mainWalletData));
    } else {
      const cusWalletData = JSON.parse(localStorage.getItem(`${customWallet}_${user}`)) || { formName: "", formValue: 0 };
      if(cusWalletData) {
          if (transType.value === 'Income') {
            cusWalletData.formValue += Number(amount.value);
          } else {
            cusWalletData.formValue -= Number(amount.value);
          }
        localStorage.setItem(`${customWallet}_${user}`, JSON.stringify(cusWalletData));
    }
  }

    } else {
      alert('error posting transaction')
    }
    } catch(e) {
      console.error('posting transaction error:', e)
    }
  }
  amount.value = ""
  desc.value = ""  
  date.value = ""
  category.value = ""
  transType.value = ""
  wallet.value = ""

}

const handleTransDelete = async (id, index) => {
   try {
    const res = await api.delete(`trans/${id}/`)  // Adjust URL as needed
    if (res.status === 204) {
      transactions.value.splice(index, 1)  // Remove from frontend
      getRecordData('trans', transactions)
    } else {
      alert("Failed to delete trans")
    }
  } catch (err) {
    console.error("Trans Delete error:", err)
    alert("Error deleting the trans row")
  }
}

const handleBudgDelete = async (id, index) => {
try {
    const res = await api.delete(`budget/${id}/`)  // Adjust URL as needed
    if (res.status === 204) {
      budgets.value.splice(index, 1)  // Remove from frontend
      getRecordData('budget', budgets)
    } else {
      alert("Failed to delete budget")
    }
  } catch (err) {
    console.error("Budget Delete error:", err)
    alert("Error deleting the budget row")
  }
}

const handleGoalDelete = async (id, index) => {
try {
    const res = await api.delete(`goal/${id}/`)  // Adjust URL as needed
    if (res.status === 204) {
      goals.value.splice(index, 1)  // Remove from frontend
      getRecordData('goal', goals)
    } else {
      alert("Failed to delete goal")
    }
  } catch (err) {
    console.error("Goal Delete error:", err)
    alert("Error deleting the goal row")
  }
}


function getWalletNameById(id) { // used to map fetched wallet id to either main or custom wallet
  const mainWalletData = JSON.parse(localStorage.getItem(`${mainWallet}_${user}`));
  const customWalletData = JSON.parse(localStorage.getItem(`${customWallet}_${user}`));
  const mainId = localStorage.getItem(`${MAIN_WALLET_ID}_${user}`)
  const customId = localStorage.getItem(`${CUS_WALLET_ID}_${user}`)

  if(mainWalletData) {
  mainWalletName = mainWalletData.formName;
  }

  if(customWalletData) {
  customWalletName = customWalletData.formName;
  }

  if (String(id) === mainId && mainWalletData && mainId) {
    return mainWalletName;
  }
  if (String(id) === customId && customWalletData && customId) {
    return customWalletName;
  }
  return "Unknown Wallet";
}

const putGoal = async (goal_id, newAmount) => { //update goal's current amount
  try {
      await api.put(`goal/${goal_id}/`, {
      current_amount: newAmount,
    });
    
  } catch (e) {
    console.error('editing goal error:', e);
  }
}

onMounted (() => {
   getRecordData('trans', transactions)
   getRecordData('budget', budgets)
   getRecordData('goal', goals)
})

</script>

<template>
  <!--Main wrapper-->
  <div class="bg-primary relative border rounded-2xl p-6 h-130">
    <!--Table title-->
    <div class="space-y-3">
      <h1 class="font-bold">{{ title }}</h1> <!--props passed for a custom title and subtitle -->
      <p class="">{{ subtitle }}</p>
    </div>
    <!--Input area to add a new row-->
    <div class="grid grid-cols-1 sm:grid-cols-7 gap-4 pb-6 pt-4 ">
      <input type="text" v-model="currAmount" placeholder="Current Amount" @input="sanitizeNums" class="border rounded border-border bg-muted placeholder:text-text px-3 py-1" v-if="isGoalsTable"> <!--Placeholder for amount changes if it's a goal table-->

      <input type="text" v-model="amount" step="any" placeholder="Amount" @input="sanitizeNums" class="border rounded px-3 py-1 text-black bg-muted placeholder:text-text" v-else>
      <input type="text" v-model="desc" placeholder="Describtion" @input="sanitizeDesc" class="border rounded px-3 py-1 text-black  bg-muted placeholder:text-text">
      <input type="date" v-model="date" class="border border-border rounded px-3 py-1  bg-muted text-text">

      <select class="border border-border rounded px-3 py-0.5  text-text focus:outline-none focus:ring-1 bg-muted placeholder:text-text" v-model="category">
        <option disabled hidden value="">Select Category</option>
        <option value="Salary">Salary</option>
        <option value="Bonus">Bonus</option>
        <option value="Business">Business</option>
        <option value="Shopping">Shopping</option>
        <option value="Debt">Debt</option>
        <option value="Other">Other</option>
      </select>

      <!--Only if goal table conditional is met-->
      <input type="text" v-model="targetAmount" placeholder="Target Amount" @input="sanitizeNums" class="border rounded  bg-muted placeholder:text-text px-3 py-1" v-if="isGoalsTable">

      <input type="date" v-model="targetDate" class="border border-border rounded px-3 py-1 bg-muted text-text" v-if="isGoalsTable">

      <!--Only if transaction table conditional is met-->
      <select class="border border-border rounded px-3 py-0.5  text-text focus:outline-none focus:ring-1  bg-muted placeholder:text-text" v-if="isTransTable" v-model="transType">
        <option disabled hidden value="">Select Transaction</option>
        <option value="Income">Income</option>
        <option value="Expense">Expense</option>
      </select>
      <select class="border border-border rounded px-3 py-0.5  text-text focus:outline-none focus:ring-1  bg-muted placeholder:text-text" v-if="isTransTable" v-model="wallet">
        <option disabled hidden value="">Select Wallet</option>
        <option :value="mainWalletName" v-if="mainWalletData">{{ mainWalletName }}</option>
        <option :value="customWalletName" v-if="customWalletData">{{ customWalletName }}</option>
      </select>
      

      <button @click="handleTransCreate" class="bg-muted border border-border rounded text-text" v-if="isTransTable"> Create +</button>
      <button @click="handleBudgCreate" class="bg-muted border border-border rounded text-text" v-if="isBudgetTable"> Create +</button>
      <button @click="handleGoalCreate" class="bg-muted border border-border rounded text-text" v-if="isGoalsTable"> Create +</button>
      <div v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</div>
    </div>
    <!--Table-->
    <div class="overflow-y-scroll max-h-[380px] ">
      <table class="w-full text-sm text-left border-collapse">
        <thead class="bg-primary sticky top-0 z-10">
          <tr>
            <th class="px-4 py-2" v-for="value in headersArr">{{ value }}</th> <!--dynamically adjusting headers titles using props-->
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <!--transaction table rows-->
          <tr v-for="(item, index) in transactions" :key="item.id" v-if="isTransTable"> 
            <td class="px-4 py-2">{{ item.amount }}</td>
            <td class="px-4 py-2">{{ item.trans_type }}</td>
            <td class="px-4 py-2">{{ getWalletNameById(item.wallet) }}</td>
            <td class="px-4 py-2">{{ item.trans_date }}</td>
            <td class="px-4 py-2">{{ item.category }}</td>
            <td class="px-4 py-2">{{ item.desc }}</td>
            <td class="px-4 py-2">
             <button @click="handleTransDelete(item.id, index)" v-if="isTransTable"><Icon icon="mdi:delete-forever" width="24" height="24" style="color: #b72c2c" /></button>
             </td>
          </tr>
          <!--budget table rows-->
          <tr v-for="(item, index) in budgets" :key="item.id" v-if="isBudgetTable"> 
            <td class="px-4 py-2">{{ item.amount }}</td>
            <td class="px-4 py-2">{{ item.budg_date }}</td>
            <td class="px-4 py-2">{{ item.category }}</td>
            <td class="px-4 py-2">{{ item.desc }}</td>
            <td class="px-4 py-2">
             <button @click="handleBudgDelete(item.id, index)" v-if="isBudgetTable"><Icon icon="mdi:delete-forever" width="24" height="24" style="color: #b72c2c" /></button>
             </td>
          </tr>
           <!--goal table rows-->
          <tr v-for="(item, index) in goals" :key="item.id" v-if="isGoalsTable"> 
            <td class="px-4 py-2">
            <input type="text" :placeholder="item.current_amount" @input="sanitizeNums" class="placeholder:text-black border border-border p-1 rounded" v-model.number="goalUpdate" @change="() => putGoal(item.id, goalUpdate)">
            </td>
            <td class="px-4 py-2">{{ item.start_date }}</td>
            <td class="px-4 py-2">{{ item.category }}</td>
            <td class="px-4 py-2">{{ item.target_amount }}</td>
            <td class="px-4 py-2">{{ item.target_date }}</td>
            <td class="px-4 py-2">{{ item.desc }}</td>
             <!--goal progress bar--> 
            <td class="px-4 py-2 w-40">
              <div class="w-full bg-gray-200 rounded h-4">
                <div
                  class="bg-surface h-4 rounded"
                  :style="{ width: ((item.current_amount / item.target_amount) * 100) + '%', maxWidth: 100 +'%' }"
                ></div>
              </div>
              <div class="text-xs text-black mt-1 text-center">
                {{ Math.round((item.current_amount / item.target_amount) * 100) <= 100 ? Math.round((item.current_amount / item.target_amount) * 100) : 100 }}%
              </div>
            </td>
            <td class="px-4 py-2">
             <button @click="handleGoalDelete(item.id , index)" v-if="isGoalsTable"><Icon icon="mdi:delete-forever" width="24" height="24" style="color: #b72c2c" /></button>
             </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
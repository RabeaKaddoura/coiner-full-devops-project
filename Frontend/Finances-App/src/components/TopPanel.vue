<script setup>
import { Icon } from "@iconify/vue";
import { onMounted, nextTick } from "vue";
import BalanceCard from "./BalanceCard.vue";
import { Username, customWallet, mainWallet, MAIN_WALLET_ID, CUS_WALLET_ID, isLoggedIn } from "@/constants";
import api from "@/api";
import { ref } from "vue";


const user = localStorage.getItem(Username)
const isLogged = localStorage.getItem(isLoggedIn)


const error = ref('')

const showForm = ref(false) //a form for custom wallet data

const formName = ref("") //these two variables hold whatever is typed into the form
const formValue = ref()

const isCustom = ref(false); //controls whether the custom wallet is displayed or not

const customWalletValue = ref(0); //data for displayed custom wallet
const customWalletName = ref("")

const mainWalletValue = ref(0); //data for displayed main wallet
const mainWalletName = ref("")

const editTarget = ref(""); // true for main wallet, false for custom. Used to specify which wallet to edit



const getWallet = async (wallet, wallet_type) => { //fetching wallet from backend
if(wallet) { //wallet represents wallet id that is stored in localstorage
try {
    const res = await api.get(`wallet/${wallet}/`);

    if(res.status === 200) {
      if(wallet_type === 'main') { //checking wallet type
      mainWalletValue.value = res.data.balance,
      mainWalletName.value = res.data.name
      } else {
        customWalletValue.value = res.data.balance
        customWalletName.value = res.data.name
      }
    } else {
      alert('error fetching wallet')
    }
    } catch(e) {
      console.error('fetching wallet error:', e)
    }
  }
}



const postWallet = async (stor_key) => { //posting wallet to backend
try {
    const res = await api.post('wallet/', {
      name: formName.value ? formName.value : "Main",
      balance: formValue.value
    });

    if(res.status === 201) {
      
      localStorage.setItem(stor_key, res.data.id);
    } else {
      console.error('posting wallet error:')
    }
    } catch(e) {
      console.error('posting wallet error:', e)
    }
}

const putWallet = async (wallet, name, balance) => { //editing wallet in backend
if(wallet) { //wallet represents wallet id that is stored in localstorage
try {
    const res = await api.put(`wallet/${wallet}/`, {
      name:  name,
      balance: balance 
    });

    } catch(e) {
      console.error('editing wallet error:', e)
    }
  }
}

const deleteWallet = async (wallet) => { //deleting custom wallet from backend
if(wallet) { //wallet represents wallet id that is stored in localstorage
try {
    const res = await api.delete(`wallet/${wallet}/`);

    if(res.status === 204) {
      
    } else {
      alert('error deleting custom wallet')
    }
    } catch(e) {
      console.error('deleting wallet error:', e)
    }
  }
}


onMounted(() => {
  // Load main wallet data
  
  const mainWalletRaw = localStorage.getItem(`${mainWallet}_${user}`); //fetching main wallet data from localStorage
  let mainWalletData = null;
  if (mainWalletRaw) {
    try {
      mainWalletData = JSON.parse(mainWalletRaw);
    } catch (e) {
      mainWalletData = null;
      console.error("Invalid main wallet data in localStorage:", mainWalletRaw);
    }
  }
  if (mainWalletData && mainWalletData.formName != null && mainWalletData.formValue != null) {
  mainWalletValue.value = Number(mainWalletData.formValue);
  mainWalletName.value = mainWalletData.formName;
} else {
  mainWalletName.value = "Main";
  mainWalletValue.value = 0;
}

  const main_w_id = localStorage.getItem(`${MAIN_WALLET_ID}_${user}`) // put and get requests made only after fetching updated data from localStorage
  if(user && isLogged && main_w_id && mainWalletData) {
    putWallet(main_w_id, "Main", mainWalletData.formValue) 
    getWallet(main_w_id, 'main') 
  }

  // Load custom wallet data
  const customWalletRaw = localStorage.getItem(`${customWallet}_${user}`);
  let customWalletData = null;
  if (customWalletRaw) {
    try {
      customWalletData = JSON.parse(customWalletRaw);
    } catch (e) {
      customWalletData = null;
      console.error("Invalid custom wallet data in localStorage:", customWalletRaw);
    }
  }
  if (customWalletData && customWalletData.formName != null && customWalletData.formValue != null) {
    isCustom.value = true;
    customWalletValue.value = Number(customWalletData.formValue);
    customWalletName.value = customWalletData.formName;
  }

   const custom_w_id = localStorage.getItem(`${CUS_WALLET_ID}_${user}`)
  if(user && isLogged && custom_w_id && customWalletData) {
    putWallet(custom_w_id, customWalletData.formName, customWalletData.formValue)
    getWallet(custom_w_id, 'custom')  
  }
});


const customWalletCreate = async () => { //creates custom wallet 
  let custom_w_id = localStorage.getItem(`${CUS_WALLET_ID}_${user}`) //wallet id used to make a PUT request to the backend
if( !formName.value || !formValue.value) {
    error.value = 'Please fill in all the fields'
    return
} 
else {
error.value = ""
localStorage.setItem(`${customWallet}_${user}`, JSON.stringify({formName: formName.value, formValue: Number(formValue.value)}))
if(user && isLogged) {
  if(!custom_w_id) { //if there's no custom wallet id stored then it must be a post request
  await postWallet(`${CUS_WALLET_ID}_${user}`) 
  custom_w_id = localStorage.getItem(`${CUS_WALLET_ID}_${user}`) //updated value of the id
  if(custom_w_id) {
  await getWallet(custom_w_id, 'custom') //immediate wallet value update
  } 
  } else { // otherwise if there's already a stored wallet id then it should be an put request (edit)
    await putWallet(custom_w_id, formName.value, formValue.value)
    await getWallet(custom_w_id, 'custom') //immediate wallet value update 
  }
}
customWalletValue.value = formValue.value
customWalletName.value = formName.value
showForm.value = false 
isCustom.value = true
formName.value = " "
formValue.value = null
}
}


const mainWalletCreate = async () => { //main wallet in storage
  const main_w_id = localStorage.getItem(`${MAIN_WALLET_ID}_${user}`)
  if(!formValue.value) {
    error.value = 'Please fill in all the fields'
    return
} 
else {
  error.value = ""
  localStorage.setItem(`${mainWallet}_${user}`, JSON.stringify({formName: "Main", formValue: Number(formValue.value)}))

  if(user && isLogged) {
    if(!main_w_id) { //if there's no main wallet id stored then it must be a post request
    await postWallet(`${MAIN_WALLET_ID}_${user}`) 
    const main_w_id = localStorage.getItem(`${MAIN_WALLET_ID}_${user}`)
    await getWallet(main_w_id, 'main') //immediate wallet value update
    } else { // otherwise if there's already a stored wallet id then it should be an put request (edit)
     await putWallet(main_w_id, "Main", formValue.value)
     await getWallet(main_w_id, 'main') //immediate wallet value update
    }
}
  mainWalletValue.value = formValue.value
  mainWalletName.value = "Main"
  showForm.value = false
  formName.value = ""
  formValue.value = null
  editTarget.value = ""
}
}


const removeCustom = async() => {
  const custom_w_id = localStorage.getItem(`${CUS_WALLET_ID}_${user}`)
  
  // Do cleanup BEFORE removing from DOM
  localStorage.removeItem(`${customWallet}_${user}`)
  localStorage.removeItem(`${CUS_WALLET_ID}_${user}`)
  
  if(custom_w_id && user && isLogged) {
    await deleteWallet(custom_w_id)
  }
  
  // Wait a tick to ensure any pending operations complete
  await nextTick();
  
  // Now safely remove from DOM
  isCustom.value = false
}

const onCloseForm = () => { //clears form data when form is closed
  editTarget.value = ""
  error.value = ""
  showForm.value = false
  formName.value = ""
  formValue.value = null
}

const handleMainEdit = () => { 
  editTarget.value = "main"
  showForm.value = true;
};

const handleCustomEdit = () => {
  editTarget.value = "custom"
  showForm.value = true;
};


const sanitizeValue= () => { //sanitizes amount input e.g. wallet value
  formValue.value = formValue.value.replace(/[^0-9]/g, '')
}

const sanitizeTitle= () => { //sanitizes title text 
   formName.value = formName.value.replace(/[<>\/\\{}\[\]]/g, '')
}




</script>

<template>
  <div class="p-6 bg-background min-h-[18rem]">
    <!-- Welcome Message -->
    <h1 v-if="user" class="mb-6 text-lg text-text font-bold">Welcome, {{ user }}.</h1>
    <h1 v-else class="mb-6 text-lg text-text font-bold">Login To Save Data.</h1>

    <!-- Wallet Cards -->
    <div class="flex gap-7 flex-wrap">
      <!-- Main Wallet Card -->
      <BalanceCard
        title="Current Balance"
        :walletName="mainWalletName"
        :value="mainWalletValue"
        @edit="handleMainEdit"
      />

      <!-- Create Wallet Button --> 
      <button
        v-if="!isCustom"
        @click="handleCustomEdit"
        class="bg-surface hover:bg-hover-bg hover:text-hover-text  p-6 rounded-2xl shadow-md w-60 max-w-md text-text font-medium text-lg"
      >
          + Create Wallet
      </button>

      <!-- Custom Wallet -->
      <BalanceCard
        v-if="isCustom"
        @removeCustom="removeCustom"
        @edit="handleCustomEdit"
        :walletName="customWalletName"
        title="Current Balance"
        :isCustom="true"
        :value=" customWalletValue"
      />
    </div>

    <!-- Modal Form -->
    <div
      v-if="showForm"
      class="fixed inset-0 backdrop-blur-sm bg-background/80 flex items-center justify-center z-50 transition-all"
    >
      <div class="bg-surface rounded-xl shadow-lg p-6 w-full max-w-sm relative">
        <!-- Close Button -->
        <button
          @click="onCloseForm"
          class="absolute top-3 right-3 text-muted hover:text-danger text-2xl font-bold"
        >
          ×
        </button>

        <h2 class="text-text text-xl font-bold mb-4">Enter Wallet Data</h2>

        <!-- Wallet Name -->
        <input
          v-if="editTarget === 'custom'"
          v-model="formName"
          placeholder="Wallet Title"
          @input="sanitizeTitle"
          class="w-full mb-3 px-3 py-2 border border-border bg-background text-text rounded focus:outline-none focus:ring-2 focus:border-border placeholder:text-text"
        />

        <!-- Wallet Value -->
        <input
          v-model="formValue"
          type="text"
          placeholder="Value"
          @input="sanitizeValue"
          class="w-full mb-4 px-3 py-2 border border-border bg-background text-text rounded focus:outline-none focus:ring-2 focus:border-border placeholder:text-text"
        />

        <div v-if="error" class="text-danger text-sm mb-4">{{ error }}</div>

        <button
          @click="editTarget === 'main' ? mainWalletCreate() : customWalletCreate()"
          class="w-full text-text bg-surface border border-border rounded text-sm mr-4 p-2 px-4 transition-colors hover:bg-hover-bg hover:text-hover-text"
        >
          Done
        </button>
      </div>
    </div>
  </div>
</template>
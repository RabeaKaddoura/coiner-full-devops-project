<script setup>
import { mainWallet, customWallet, Username, isLoggedIn, MAIN_WALLET_ID, CUS_WALLET_ID } from '@/constants';
import { onMounted, ref, computed, watch } from 'vue';
import { Icon } from "@iconify/vue";
import api from '@/api';
import { Bar, Pie, Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  LineElement,
  PointElement
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement, PointElement);

const user = localStorage.getItem(Username)

const transactions = ref([])
const goals = ref([])

const transCategory = ref(['Salary', 'Bonus', 'Business', 'Shopping', 'Debt', 'Other'])
const expenses = ref([])

const totalMainWallet = ref(0)
const totalCusWallet = ref(0)

const incomeData = ref(new Array(12).fill(0)); //we make two arrays of fixed length (12) which align with the year's months. They need to align with the amount of months
const expenseData = ref(new Array(12).fill(0)); //so that they're properly displayed on the bar chart where each month has two bars, one for income and one for expense



const isFetched = ref(false);


function getWalletNameById(id) { // used to map fetched wallet id to either main or custom wallet
  const mainId = localStorage.getItem(`${MAIN_WALLET_ID}_${user}`)
  const customId = localStorage.getItem(`${CUS_WALLET_ID}_${user}`)
  
  if (String(id) === mainId) {
    return "Main";
  }
  if (String(id) === customId) {
    return "Custom";
  }
  return "Unknown Wallet";
}

onMounted(async () => { //fetching data from backend
if (transactions.value.length === 0) {
    try {
    const res = await api.get('trans/');
    transactions.value = res.data;
    isFetched.value = true;
    } catch(e) {
        console.log("error fetching for reports: ", e)
    }
  }

  if (goals.value.length === 0) {
    try {
    const res = await api.get('goal/');
    goals.value = res.data;
  } catch(e) {
      console.log("error fetching for reports: ", e)
    }
  }
})


watch([isFetched, transactions], (val) => { //once data are retrieved from backend, build charts' data. 
//Bar data
  if (val) {
    const categoryTotals = {};
    transCategory.value.forEach(cat => {
      categoryTotals[cat] = 0; //key-value pairs for each category (value = amount of expense)
    });

    // Aggregate totals by category using fetched transactions
    transactions.value.forEach(trans => {
      if (trans.trans_type === 'Expense' && categoryTotals.hasOwnProperty(trans.category)) { //checking if the category exists and whether transaction type is expense
        categoryTotals[trans.category] += parseFloat(trans.amount); //incrementing category using the key 
      }
    });
    expenses.value = transCategory.value.map(cat => categoryTotals[cat] || 0); //extracting each categories' aggregated expenses 
  }

  //Pie data
  totalMainWallet.value = 0 //resetting totals
  totalCusWallet.value = 0
  transactions.value.forEach(trans => {
    const walletName = getWalletNameById(trans.wallet) 
      if (trans.trans_type === 'Expense') { //checking if the transaction type is expense
        if(walletName === 'Main') { //incrementing main wallet total
        totalMainWallet.value += parseFloat(trans.amount); //incrementing category using the key 
        } else { //incrementing custom wallet total
          totalCusWallet.value += parseFloat(trans.amount);
        }
      }
    });

    //Months data
     incomeData.value = new Array(12).fill(0); //resetting values
     expenseData.value = new Array(12).fill(0);
    transactions.value.forEach(trans => {
      const date = trans.created_on.slice(0, 10) // yy//mm//dd format
      const monthIndex = parseInt(date.split('-')[1], 10) - 1; //month index (0-11)
      const amount = parseFloat(trans.amount);

       if (trans.trans_type === 'Income') {
          incomeData.value[monthIndex] += amount;
      } else if (trans.trans_type === 'Expense') {
          expenseData.value[monthIndex] += amount;
       }
    });

    //line chart data
    transactions.value.forEach(trans => {
      
    });
});


const barChartData = computed(() => ({
  labels: transCategory.value,  
  datasets: [
    {
      label: 'Expenses',
      backgroundColor: '#f87171',
      data: expenses.value,
    },
  ],
}));

const barChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: 'var(--color-text)', // color of  labels
      },
    },
    title: {
      display: true,
      text: 'Expenses By Category',
      color: 'var(--color-text)', // chart title color
      font: {
        size: 16,
        weight: 'bold',
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: 'var(--color-muted)', // X-axis labels
      },
      
    },
    y: {
      ticks: {
        color: 'var(--color-muted)', // Y-axis numbers
      },
    },
  },
};

const pieChartData = computed(() => ({
  labels: ['Main Wallet', 'Custom Wallet'],
  datasets: [
    {
      label: 'Expenses',
      data: [totalMainWallet.value || 0, totalCusWallet.value || 0], 
      backgroundColor: ['#60a5fa', '#fbbf24'],
    },
  ],
}));

const pieChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: 'var(--color-text)', // color of labels
      },
    },
    title: {
      display: true,
      text: 'Expenses by Wallet',
      color: 'var(--color-text)', // chart title color
      font: {
        size: 16,
        weight: 'bold',
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: 'var(--color-muted)', // X-axis labels
      },
      
    },
    y: {
      ticks: {
        color: 'var(--color-muted)', // Y-axis numbers
      },
    },
  },
};

const monthChartData = computed(() => ({
  labels: [ "Jan", "Feb", "March", "April", "May", "June",
  "July", "Aug", "Sep", "Oct", "Nov", "Dec"],  
  datasets: [
    {
      label: 'Income',
      backgroundColor: '#4ade80',
      data: incomeData.value,
    },
    {
      label: 'Expense',
      backgroundColor: '#f87171',
      data: expenseData.value,
    },
  ],
}));

const monthChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: 'var(--color-text)', // color  labels
      },
    },
    title: {
      display: true,
      text: 'Monthly Income vs Expense (Actual Date)',
      color: 'var(--color-text)', // chart title color
      font: {
        size: 16,
        weight: 'bold',
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: 'var(--color-muted)', // X-axis labels
      },
      
    },
    y: {
      ticks: {
        color: 'var(--color-muted)', // Y-axis numbers
      },
    },
  },
};

</script>

<template>
  <!--First chart row-->
<div class="flex gap-20">
<div class="bg-primary p-6 rounded border shadow-md flex-1">
    <Bar :data="barChartData" :options="barChartOptions" style="height: 400px" />
  </div>
  <div class="bg-primary p-6 rounded border shadow-md flex-1 flex justify-center">
    <Pie :data="pieChartData" :options="pieChartOptions" style="height: 400px" />
  </div>
</div>
<!--Second chart row-->
<div class="flex gap-20">
<div class="bg-primary p-3 rounded border shadow-md flex-1 w-[800px] h-[700px] flex justify-center">
    <Bar :data="monthChartData" :options="monthChartOptions" class="w-full h-full" />
  </div>
</div>
</template>
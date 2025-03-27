<template>
  <div class="container">
    <div class="header">
      <h1>Busca de Operadoras de Saúde</h1>
      <div class="search-box">
        <input
          v-model="searchTerm"
          @input="handleSearch"
          @keyup.enter="fetchData"
          placeholder="Digite razão social, CNPJ ou cidade..."
        />
        <button @click="fetchData">
          <i class="search-icon">🔍</i> Buscar
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-message">
      <div class="spinner"></div>
      <p>Carregando resultados...</p>
    </div>

    <div v-if="error" class="error-message">
      <p>⚠️ {{ error }}</p>
      <button @click="fetchData" class="retry-button">Tentar novamente</button>
    </div>

    <div v-if="results.length > 0" class="results-container">
      <div class="summary">
        <p v-if="totalResults > MAX_RESULTS">
          Mostrando {{ MAX_RESULTS }} de {{ totalResults }} operadoras encontradas
        </p>
        <p v-else>
          {{ totalResults }} operadora{{ totalResults !== 1 ? 's' : '' }} encontrada{{ totalResults !== 1 ? 's' : '' }}
        </p>
      </div>
      
      <div v-for="(item, index) in results" :key="index" class="result-item">
        <div class="result-content">
          <h3>{{ item.Razao_Social || 'Nome não disponível' }}</h3>
          <div class="operadora-details">
            <p><strong>Nome Fantasia:</strong> {{ item.Nome_Fantasia || '-' }}</p>
            <p><strong>CNPJ:</strong> {{ formatCNPJ(item.CNPJ) }}</p>
            <p><strong>Localização:</strong> {{ item.Cidade || 'Cidade não informada' }}/{{ item.UF || 'UF não informada' }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="searchPerformed && !loading" class="no-results">
      <p>Nenhuma operadora encontrada para "{{ searchTerm }}"</p>
      <p v-if="totalResults > MAX_RESULTS" class="tip">
        Dica: Tente refinar sua busca para obter resultados mais específicos
      </p>
    </div>
  </div>
</template>

<script>
const MAX_RESULTS = 20;

export default {
  data() {
    return {
      searchTerm: '',
      results: [],
      totalResults: 0,
      loading: false,
      error: null,
      debounceTimer: null,
      searchPerformed: false,
      MAX_RESULTS: MAX_RESULTS
    }
  },
  methods: {
    formatCNPJ(cnpj) {
      if (!cnpj || cnpj === '') return 'Não disponível'
      // Remove caracteres não numéricos
      const cleaned = cnpj.toString().replace(/\D/g, '')
      // Formata: 00.000.000/0000-00
      return cleaned.replace(
        /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
        '$1.$2.$3/$4-$5'
      )
    },
    handleSearch() {
      clearTimeout(this.debounceTimer)
      this.debounceTimer = setTimeout(() => {
        this.fetchData()
      }, 500)
    },
    async fetchData() {
      if (!this.searchTerm.trim()) {
        this.results = []
        this.totalResults = 0
        this.searchPerformed = false
        return
      }

      this.loading = true
      this.error = null
      this.searchPerformed = true

      try {
        const response = await fetch(
          `http://localhost:5000/api/buscar?q=${encodeURIComponent(this.searchTerm)}`
        )
        
        if (!response.ok) {
          throw new Error(`Erro na busca: ${response.statusText}`)
        }

        const data = await response.json()
        
        if (data.success) {
          this.results = data.results || []
          this.totalResults = data.count || 0
        } else {
          throw new Error(data.error || 'Erro desconhecido na resposta da API')
        }
      } catch (err) {
        console.error('Erro na requisição:', err)
        this.error = err.message || 'Erro ao buscar operadoras'
        this.results = []
        this.totalResults = 0
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  margin-bottom: 2rem;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.search-box {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

input {
  padding: 0.75rem 1rem;
  width: 100%;
  max-width: 500px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #3aa876;
}

.search-icon {
  font-size: 1rem;
}

.loading-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #42b983;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  text-align: center;
  color: #e74c3c;
  margin: 2rem 0;
}

.retry-button {
  margin-top: 1rem;
  background-color: #e74c3c;
}

.retry-button:hover {
  background-color: #c0392b;
}

.results-container {
  margin-top: 2rem;
}

.summary {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #7f8c8d;
}

.result-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.result-item:hover {
  transform: translateY(-2px);
}

.result-content h3 {
  margin-top: 0;
  color: #2c3e50;
}

.operadora-details {
  margin-top: 0.75rem;
}

.operadora-details p {
  margin: 0.5rem 0;
  color: #34495e;
}

.no-results {
  text-align: center;
  margin: 2rem 0;
  color: #7f8c8d;
}

.tip {
  font-style: italic;
  margin-top: 1rem;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
  
  .search-box {
    flex-direction: column;
    align-items: center;
  }
  
  button {
    width: 100%;
    max-width: 500px;
  }
}
</style>
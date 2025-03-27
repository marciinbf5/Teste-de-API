<template>
  <div class="container">
    <div class="header">
      <h1>Busca de Operadoras de Saúde</h1>
      <div class="search-box">
        <input
          v-model="searchTerm"
          @input="handleSearch"
          placeholder="Digite razão social, CNPJ ou cidade..."
        />
        <button @click="fetchData">
          <i class="search-icon">🔍</i> Buscar
        </button>
      </div>
    </div>

    <div v-if="loading" class="item loading">
      <i>
        <slot name="icon">⏳</slot>
      </i>
      <div class="details">
        <h3>
          <slot name="heading">Carregando...</slot>
        </h3>
        <slot>Por favor, aguarde enquanto buscamos os dados.</slot>
      </div>
    </div>

    <div v-if="error" class="item error">
      <i>
        <slot name="icon">⚠️</slot>
      </i>
      <div class="details">
        <h3>
          <slot name="heading">Erro na busca</slot>
        </h3>
        <slot>{{ error }}</slot>
      </div>
    </div>

    <div v-if="results.length > 0" class="results-container">
      <div class="summary">
        <p>Total encontrado: {{ totalResults }} operadoras</p>
      </div>
      
      <div v-for="(item, index) in results" :key="index" class="item result-item">
        <i>
          <slot name="icon">🏥</slot>
        </i>
        <div class="details">
          <h3>
            <slot name="heading">{{ item.Razao_Social || 'Nome não disponível' }}</slot>
          </h3>
          <div class="operadora-details">
            <p><strong>Nome Fantasia:</strong> {{ item.Nome_Fantasia || 'Não disponível' }}</p>
            <p><strong>CNPJ:</strong> {{ formatCNPJ(item.CNPJ) }}</p>
            <p><strong>Localização:</strong> {{ item.Cidade || 'Cidade não informada' }}/{{ item.UF || 'UF não informada' }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="searchTerm && !loading" class="item no-results">
      <i>
        <slot name="icon">🔍</slot>
      </i>
      <div class="details">
        <h3>
          <slot name="heading">Nenhum resultado encontrado</slot>
        </h3>
        <slot>Não encontramos operadoras para "{{ searchTerm }}"</slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: '',
      results: [],
      totalResults: 0,
      loading: false,
      error: null,
      debounceTimer: null
    }
  },
  methods: {
    formatCNPJ(cnpj) {
      if (!cnpj) return 'Não disponível'
      // Formatação básica de CNPJ: 00.000.000/0000-00
      return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5')
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
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await fetch(
          `http://localhost:5000/api/buscar?q=${encodeURIComponent(this.searchTerm)}`
        )
        
        if (!response.ok) {
          throw new Error(`Erro ${response.status}: ${response.statusText}`)
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
        this.error = err.message
        this.results = []
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  margin-bottom: 2rem;
  text-align: center;
}

h1 {
  color: var(--color-heading);
  margin-bottom: 1rem;
}

.search-box {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

input {
  padding: 0.75rem;
  width: 400px;
  max-width: 100%;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 1rem;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: var(--color-button-bg);
  color: var(--color-button-text);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

button:hover {
  background-color: var(--color-button-hover);
}

.search-icon {
  font-size: 1rem;
}

.results-container {
  margin-top: 2rem;
}

.summary {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.1rem;
  color: var(--color-text);
}

.operadora-details {
  margin-top: 0.5rem;
}

.operadora-details p {
  margin: 0.25rem 0;
  color: var(--color-text);
}

.item {
  margin-top: 1.5rem;
}

.loading i {
  color: var(--color-loading);
}

.error i {
  color: var(--color-error);
}

.no-results i {
  color: var(--color-text-muted);
}

@media (max-width: 768px) {
  .search-box {
    flex-direction: column;
    align-items: center;
  }
  
  input {
    width: 100%;
  }
}
</style>
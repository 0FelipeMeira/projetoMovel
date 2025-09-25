# DoseCerta

Aplicativo mobile em React Native para controle de horários de medicamentos, pensado especialmente para idosos e seus cuidadores/familiares. O objetivo é garantir que os medicamentos sejam tomados corretamente, oferecendo lembretes com alarmes sonoros e acompanhamento remoto pelos filhos ou responsáveis.

## Funcionalidades

- **Cadastro de Usuários:** Permite que filhos/responsáveis criem perfis para os idosos.
- **Cadastro de Medicamentos:** Adicione/remova medicamentos, defina dosagem, horários e frequência.
- **Alarmes e Lembretes:** Notificações locais com alarme para lembrar o idoso de tomar o remédio na hora certa.
- **Confirmação de Tomada:** O idoso pode marcar se tomou o medicamento, gerando um histórico.
- **Acompanhamento Remoto:** Filhos podem acompanhar o histórico de tomadas e receber notificações caso haja esquecimento.
- **Interface Simples e Acessível:** Layout adaptado para facilitar o uso por idosos.

## Tecnologias Utilizadas

- [React Native](https://reactnative.dev/)
- [Expo](https://expo.dev/) (opcional)
- [AsyncStorage](https://react-native-async-storage.github.io/async-storage/) ou [SQLite](https://docs.expo.dev/versions/latest/sdk/sqlite/) para armazenamento local
- [Firebase](https://firebase.google.com/) (autenticação e sincronização de dados)
- [react-native-push-notification](https://github.com/zo0r/react-native-push-notification) ou [expo-notifications](https://docs.expo.dev/versions/latest/sdk/notifications/) para alarmes

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/0FelipeMeira/project-native.git
   cd project-native
   ```

2. **Instale as dependências:**
   ```bash
   npm install
   # ou
   yarn install
   ```

3. **Configure variáveis de ambiente:**
   - Crie um arquivo `.env` e adicione as chaves necessárias (Firebase, etc).

4. **Execute o projeto:**
   ```bash
   npx expo start
   # ou
   npm run android
   # ou
   npm run ios
   ```

## Estrutura do Projeto

```
project-native/
├── src/
│   ├── components/
│   ├── screens/
│   ├── services/
│   └── utils/
├── App.js
├── package.json
└── ...
```

## Como Contribuir

1. Fork este repositório.
2. Crie uma branch para sua feature/bugfix:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça commit de suas alterações.
4. Envie um Pull Request.

---

**DoseCerta** — Mais segurança e tranquilidade para famílias e idosos no controle dos medicamentos!
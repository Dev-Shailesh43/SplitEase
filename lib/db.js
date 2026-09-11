/**
 * lib/db.js
 * 
 * Mock Database adapter for the new Node.js backend.
 * In a real production environment, this would use Prisma to connect to a PostgreSQL database.
 */

// In-memory store for demonstration purposes
const dbStore = {
  users: [],
  pods: [],
  expenses: []
};

export const db = {
  users: {
    findMany: async () => dbStore.users,
    create: async (data) => {
      const newUser = { id: Date.now().toString(), ...data };
      dbStore.users.push(newUser);
      return newUser;
    }
  },
  pods: {
    findMany: async () => dbStore.pods,
    create: async (data) => {
      const newPod = { id: Date.now().toString(), ...data, members: [] };
      dbStore.pods.push(newPod);
      return newPod;
    }
  },
  expenses: {
    findMany: async (podId) => dbStore.expenses.filter(e => e.podId === podId),
    create: async (data) => {
      const newExp = { id: Date.now().toString(), ...data };
      dbStore.expenses.push(newExp);
      return newExp;
    }
  }
};

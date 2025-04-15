# Flor de Iris
# De forma adicional a lógica matriz de confusão

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, confusion_matrix

iris = load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, train_size=0.7, shuffle=True, stratify=None)
tree = DecisionTreeClassifier()
tree.fit(X_train, y_train)
y_prev = tree.predict(X_test)

accuracy = accuracy_score(y_test, y_prev)
print('Precisão: {:.2f}%'.format(accuracy*100))

print("\nMatriz de confusão:")
print(confusion_matrix(y_test, y_prev))

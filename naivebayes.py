import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

#taking input and output data values
X=pd.read_csv('reduced_features_X1.csv',header=None)
y=pd.read_csv('feature_y1.csv',header=None)

#splitting into test set and training set 
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 0)


# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

classifier.score(X_train,y_train)
classifier.score(X_test,y_test)   #accuracy


#5 fold cross validation
from sklearn.model_selection import cross_val_score
accuracies=cross_val_score(estimator=classifier,X=X_train,y=y_train,cv=5)
accuracies.mean()

#Accuracy score
from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)
classifier.score(X_train,y_train)
classifier.score(X_test,y_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


#classification reports
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

reader=csv.reader(open("feature_y1.csv","r"),delimiter=",")
y=list(reader)
y=np.array(y)
y=y.astype(np.int)
y=y.ravel()	


from sklearn.manifold.t_sne import TSNE
from sklearn.neighbors import  KNeighborsClassifier
X_Train_embedded = TSNE(n_components=2).fit_transform(X)
print (X_Train_embedded.shape)
model = classifier.fit(X,y)
y_predicted = model.predict(X)

# create meshgrid
resolution = 1024 # 100x100 background pixels
X2d_xmin, X2d_xmax = np.min(X_Train_embedded[:,0]), np.max(X_Train_embedded[:,0])
X2d_ymin, X2d_ymax = np.min(X_Train_embedded[:,1]), np.max(X_Train_embedded[:,1])
xx, yy = np.meshgrid(np.linspace(X2d_xmin, X2d_xmax, resolution), np.linspace(X2d_ymin, X2d_ymax, resolution))

# approximate Voronoi tesselation on resolution x resolution grid using 1-NN
background_model = KNeighborsClassifier(n_neighbors=1).fit(X_Train_embedded, y_predicted) 
voronoiBackground = background_model.predict(np.c_[xx.ravel(), yy.ravel()])
voronoiBackground = voronoiBackground.reshape((resolution, resolution))

#plot
plt.contourf(xx, yy, voronoiBackground)
plt.scatter(X_Train_embedded[:,0], X_Train_embedded[:,1], c=y)
plt.show()
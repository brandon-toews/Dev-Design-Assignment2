from myimports import (
    pd, sns, plt, np, train_test_split, LinearRegression, metrics,
    StandardScaler, MinMaxScaler, KNeighborsClassifier, DecisionTreeClassifier,
    classification_report, confusion_matrix, ConfusionMatrixDisplay, KMeans,
    GaussianMixture, SpectralClustering, Image, ImageDraw, ImageFont
)

np.set_printoptions(suppress=True)

# Function to capture the printed text
def print_and_save_text(text_to_save, picture_height, font_size):
    
    # Set the font and size
    font = ImageFont.truetype("Hack Regular Nerd Font Complete.ttf", font_size)

    # Create an empty image
    image = Image.new("RGB", (650, picture_height), "white")
    draw = ImageDraw.Draw(image)

    
    # Specify the position, text content, font, and fill color
    position = (10, 10)
    text = text_to_save
    print(text)
    fill_color = "black"

    # Split the text into lines
    lines = text.split("\n")

    # Draw each line of text on the image
    for i, line in enumerate(lines):
        line_position = (position[0], position[1] + i * font.size)
        draw.text(line_position, line, font=font, fill=fill_color)

    # Save the image as a JPEG file
    image.save("LinRegResults.jpg")
    
    return "LinRegResults.jpg"

def combine_images(jpg1, jpg2):
    # Open the image
        image1 = Image.open(jpg1)
        # Get the size of the image
        width1, height1 = image1.size
        
        # Open the image
        image2 = Image.open(jpg2)
        # Get the size of the image
        width2, height2 = image2.size
        
        combined_image = Image.new("RGB", (650, height1+height2), (255, 255, 255))

        # Paste the first image on the left side
        combined_image.paste(image1, (0, 0))

        # Paste the second image on the right side
        combined_image.paste(image2, (0, height1))

        # Save the combined image
        combined_image.save('results.jpg')
        
        return "results.jpg"


# Linear Regression training function that takes in X and Y arguments and displays results
def myLinRegModel(x, y, scale_selection, testSize):
    
    #string to hold results to display later
    results = ""
    results_height = 0
    
    # While loop to iterate every 10% from given test size
    while testSize>0:
        
        # Splitting data into training and testing variables using the values passed into function
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=(testSize/100), random_state=0)
        
        # Standardizes data if specified when calling function
        if scale_selection == 'Standardize':
            
            scale = scale_selection
            # Standardize features by removing mean and scaling to unit variance:
            scaler = StandardScaler()
            scaler.fit(x_train)
            x_train = scaler.transform(x_train)
            x_test = scaler.transform(x_test)

        # Normalizes data if specified when calling function
        elif scale_selection == "Normalize":
            
            scale = scale_selection
            # Normalize features by shrinking data range between 0 & 1:
            scaler = MinMaxScaler()
            scaler.fit(x_train)
            x_train = scaler.transform(x_train)
            x_test = scaler.transform(x_test)
            
        else: scale = "None"

        # Training model with LinearRegression function and training data
        regressor = LinearRegression()
        regressor.fit(x_train, y_train)
        
        
        #Add to string to display later
        results = results+"Linear Regression Model - Scaling: "+scale+"\n\n\n"
        
        # Print algorithm type and what if any scales were applied to the data
        print('Linear Regression Model - Scaling:', scale_selection, '\n')
    
    
        #Add to string to display later
        results = results+"Test Size: "+str(testSize)+"%\n\n"
        
        # Print test size of current iteration
        print('Test Size:', testSize, '%\n')

        
        #Add to string to display later
        results = results+"a = "+str(regressor.intercept_)+"\n"
        results = results+"b = "+str(np.round(regressor.coef_, 2))+"\n\n\nSample of Test Results:\n\n"
        # Print intercept and CoEfficient values of model
        print("a =", regressor.intercept_)
        print("b =", regressor.coef_)

        # Test the trained model with test data and store in variable
        y_pred = regressor.predict(x_test)

        # Display predicted values next to actual values for comparison
        df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
        print(df)
        
        #Add to string to display later
        results = results+df.head(10).to_string(index=False)+"\n\n\n"
    
        # Display accuracy of model predictions in the form of Mean Absolute Error, Mean Squared Error,
        # Root Mean Squared Error using the difference between actual and predicted values
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
        print('R2 Score: ', metrics.r2_score(y_test,y_pred)*100, '%\n', sep='')
        
        #Add to string to display later
        results = results+'Mean Absolute Error: '+str(metrics.mean_absolute_error(y_test, y_pred))+"\n"
        results = results+'Mean Squared Error: '+str(metrics.mean_squared_error(y_test, y_pred))+"\n"
        results = results+'Root Mean Squared Error: '+str(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))+"\n"
        results = results+'R2 Score: '+str(int(metrics.r2_score(y_test,y_pred)*100))+"%\n\n\n"
        
        # Decrease test size by 10
        testSize -= 10
        results_height += 650
        
    return print_and_save_text(results, results_height, 20)
        
# Classification training function that takes in X values to classify according to Y values
# and takes what scalar should be used
def myClassModel(X, y, scale_selection, method_selection, testSize):
    
    #string to hold results to display later
    results = ""
    
    # Split dataset into random train and test subsets:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(testSize/100)) 

    # Standardizes data if specified when calling function
    if scale_selection == 'Standardize':
        scale = scale_selection
        # Standardize features by removing mean and scaling to unit variance:
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
    
    # Normalizes data if specified when calling function
    elif scale_selection == "Normalize":
        scale = scale_selection
        # Normalize features by shrinking data range between 0 & 1:
        scaler = MinMaxScaler()
        scaler.fit(X_train)

        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        
    else: scale = "None"

    if method_selection == "KNeighbors":   
        # Use the KNN classifier to fit data:
        knclassifier = KNeighborsClassifier(n_neighbors=5)
        knclassifier.fit(X_train, y_train) 

        # Predict y data with KNN classifier: 
        y_predict = knclassifier.predict(X_test)

        # Print KNN classifier results:
        print("KNeighbors Classifier - Scaling:", scale)
        #Add to string to display later
        results = results+"KNeighbors Classifier - Scaling: "+scale+"\n\n"
        
        cm = confusion_matrix(y_test, y_predict, labels=knclassifier.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=knclassifier.classes_)
        disp.plot()
        plt.savefig("confusion_matrix.jpg", dpi=100)  # Save the confusion matrix plot
        
        print(classification_report(y_test, y_predict))
        #Add to string to display later
        results = results+classification_report(y_test, y_predict)
        
        return combine_images("confusion_matrix.jpg", print_and_save_text(results, 400, 17))
    
    elif method_selection == "Decision Tree":
        # Use the Decision Tree classifier to fit data:
        dtclassifier = DecisionTreeClassifier()
        dtclassifier.fit(X_train, y_train) 

        # Predict y data with Decision Tree classifier: 
        y_predict = dtclassifier.predict(X_test)

        # Print Decision Tree classifier results:
        print("Decision Tree Classifier - Scaling:", scale)
        #Add to string to display later
        results = results+"Decision Tree Classifier - Scaling: "+scale+"\n\n"
        
        cm = confusion_matrix(y_test, y_predict, labels=dtclassifier.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=dtclassifier.classes_)
        disp.plot()
        plt.savefig("confusion_matrix.jpg", dpi=100) # Save the confusion matrix plot
        
        print(classification_report(y_test, y_predict))
        #Add to string to display later
        results = results+classification_report(y_test, y_predict)
        
        return combine_images("confusion_matrix.jpg", print_and_save_text(results, 400, 15))
    
    
    
# Cluster training function that takes in X values to cluster, along with
# what model should be used and how many clusters should be created
def myClusterModel(X, scale_selection, method_selection, num_clusters):
    
    # Store columns names of features
    column_name = list(X.columns)
    # Stores feature values fro use in some models
    features = X.values
    
    # Takes given features and creates dataframe for some models
    X = pd.DataFrame(X)
    
    # Standardizes data if specified when calling function
    if scale_selection == 'Standardize':
        scale = scale_selection
        # Standardize features by removing mean and scaling to unit variance:
        scaler = StandardScaler()
        scaler.fit(features)
        scaled = scaler.transform(features)
    
    # Normalizes data if specified when calling function
    elif scale_selection == "Normalize":
        scale = scale_selection
        # Normalize features by shrinking data range between 0 & 1:
        scaler = MinMaxScaler()
        scaler.fit(features)
        scaled = scaler.transform(features)
    
    else: 
        #No Scaling
        scale = "None"
        scaled = features
    
    # For KMeans model
    if method_selection=='KMeans':
        # Initialize KMeans model with given number of clusters
        kmeans = KMeans(n_clusters=num_clusters)
        
        # Produce clusters with model and append cluster label info to DataFrame X
        X['cluster'] = kmeans.fit_predict(scaled)
        
        # Set plot size
        plt.figure(figsize=(6, 6))
        # Plot data with given features
        plt.scatter(X[column_name[0]], X[column_name[1]])

        # Plot KMeans cluster centers
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
        # Display plot
        plt.xlabel(column_name[0])
        plt.ylabel(column_name[1])
        #plt.xlim(0,31)
        #plt.ylim(0,55000)
        plt.title("KMeans Cluster Model - Scaling: "+scale)
        plt.savefig("cluster1.jpg", dpi=100)

        # Display scatter plot with KDE to see compare how well
        # model performed at creating relevant clusters
        g = sns.jointplot(data=X, x=column_name[0], y=column_name[1], hue='cluster')
        g.fig.suptitle("KMeans Cluster Model - Scaling: "+scale)
        g.plot_joint(sns.kdeplot, levels=num_clusters, warn_singular=False)
        g.savefig("cluster2.jpg", dpi=100)
        
        return combine_images("cluster1.jpg", "cluster2.jpg")
            
    # For Gaussian Mixture model    
    elif method_selection=='Gaussian Mixture':
        # Initialize Gaussian Mixture with given number of clusters
        gmm_model = GaussianMixture(n_components=num_clusters)
        gmm_model.fit(scaled)

        # Produce clusters with model and append cluster label info to DataFrame X
        X['cluster'] = gmm_model.predict(scaled)

        # Display scatter plot with KDE to see compare how well
        # model performed at creating relevant clusters
        g = sns.jointplot(data=X, x=column_name[0], y=column_name[1], hue="cluster")
        g.fig.suptitle("Gaussian Mixture Model - Scaling: "+scale)
        g.plot_joint(sns.kdeplot, levels=num_clusters, common_norm=False, warn_singular=False)
        g.savefig("cluster1.jpg", dpi=100)
        
        return "cluster1.jpg"
    
    elif method_selection=='Spectral Clustering':
        # Initialize Spectral Clustering model with given number of clusters
        sc = SpectralClustering(n_clusters=num_clusters, random_state=25, n_neighbors=25,\
        affinity='nearest_neighbors')
        
        # convert scaled values to dataframe to be used by model
        scaled = pd.DataFrame(scaled)
        
        # Appends new scaled cluster label info to DataFrame X
        X['cluster'] = sc.fit_predict(scaled[[0, 1]])
        
        # Display scatter plot with KDE to see compare how well
        # model performed at creating relevant clusters with scaled data
        g = sns.jointplot(data=X, x=column_name[0], y=column_name[1], hue="cluster")#, xlim=(0,31)
        g.fig.suptitle("Spectral Clustering Model - Scaling: "+scale)
        g.plot_joint(sns.kdeplot, levels=num_clusters, common_norm=False, warn_singular=False)
        g.savefig("cluster1.jpg", dpi=100)
        
        return "cluster1.jpg"
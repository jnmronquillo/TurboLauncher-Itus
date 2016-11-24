package ca.uwaterloo.crysp.itus.machinelearning;

/**
 * Created by R on 25/10/2016.
 */

import java.util.List;

import ca.uwaterloo.crysp.itus.FeatureVector;

/**
 * Model for the KNN Classifier
 *
 * @author Aaron Atwater
 * @author Hassan Khan
 */
@SuppressWarnings("serial")
public class KNNModel implements java.io.Serializable {
    /**
     * A reference to training and testing instances
     */
    public List<FeatureVector> data;
    /**
     * Number of nearest neighbors 'k'
     */
    public int k;

    /**
     * Number of Features for the classifier
     */
    public int numFeatures;

    /**
     * constructor for KNNModel
     * @param k Number of nearest neighbors 'k'
     * @param numFeatures Number of Features for the classifier
     */
    public KNNModel(int k, int numFeatures){
        this.k = k;
        this.numFeatures = numFeatures;
    }

    /**
     * Copy constructor for KNNModel
     * @param k Number of nearest neighbors 'k'
     * @param numFeatures Number of Features for the classifier
     */
    public KNNModel(Object objModel){
        KNNModel model = (KNNModel) objModel;
        this.k = model.k;
        this.numFeatures = model.numFeatures;
        this.data = model.data;
    }
}

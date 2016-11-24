package com.phonemetra.turbo.launcher;

import android.app.Fragment;
import android.os.Bundle;

import org.thoughtcrime.securesms.authentication.measurements.TouchEventLive;
import org.thoughtcrime.securesms.authentication.storage.PermanentStorageAndroid;

import java.util.ArrayList;
import java.util.Arrays;

import ca.uwaterloo.crysp.itus.Itus;
import ca.uwaterloo.crysp.itus.Parameters;
import ca.uwaterloo.crysp.itus.machinelearning.Classifier;
import ca.uwaterloo.crysp.itus.machinelearning.SVMClassifier;
import ca.uwaterloo.crysp.itus.measurements.TouchEvent;

/**
 * Created by R on 9/11/2016.
 */

public class ItusFragment extends Fragment {
    //private Touchalytics touchalytics;
    Itus itus;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Retain this fragment across configuration changes.
        setRetainInstance(true);

        /*Parameters.setPermanentStorageInstance(new PermanentStorageAndroid());
        TouchEventLive touchEventLive = new TouchEventLive();
        touchalytics = new Touchalytics(touchEventLive);

        Parameters.setOnlineMode();
        //Parameters.setConfigMode(new PermanentStorageAndroid());
        Parameters.setTrainingThreshold(20);

        touchalytics.start();*/

        Parameters.setPermanentStorageInstance(new PermanentStorageAndroid());
        Parameters.setConfigMode(new PermanentStorageAndroid());
        itus = new Itus();
        String[] featureList = Arrays.copyOfRange(TouchEvent.featureList, 0, 29);

        Classifier svm = new SVMClassifier(featureList.length);

        TouchEventLive touch = new TouchEventLive();
        touch.setFeatureList(featureList);
        itus.useMeasurement(touch);
        itus.useClassifier(svm);
        itus.start();
    }

    //public Touchalytics getTouchalytics() {
    //    return touchalytics;
    //}
    public boolean enoughData(){ return itus.enoughData();}
    public ArrayList<Integer> getPastScores(){return  itus.getPastScores();}
}

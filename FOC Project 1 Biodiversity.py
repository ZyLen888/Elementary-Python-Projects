def get_species_richness(observed_list):
    '''This function calculates the species richness of a habitat, 
    based on the number of different species in it
    
    Argument:
        observed_list: A list of independent observations of birds species 
                        (strings of birds name)
    
    Return:
        (species_richness, species_list): a tuple of
            species_richness: number of types of birds found in observed list
            species_list: the names of different types of birds found in list
                            (alphabetical order)    
    '''
    # To eliminate the repeated types of birds by using set 
    observed_set = set(observed_list)
    # Convert the set of types of birds back to list
    types_of_birds = list(observed_set)
    # Counts the number of different types of bird
    species_richness = len(observed_set) 
    # Sort the names of birds in alphabetical order
    species_list = sorted(types_of_birds)
    return species_richness, species_list
    
def get_species_evenness(observed_list):
    '''This function calculates the species evenness of a habitats, 
    based on a series of observations of various bird species.
    
    Argument:
        observed_list: A list of independent observations of birds species 
                        (strings of birds name)
    
    Return: 
        (species_evenness, [(species_name, species_counts)]):
        A tuple consists of: 
            species_evenness: Simpson inverse index of the observation list
            species_list: a list of (species_name, species_counts) that is 
                          sorted in alphabetical order. 
                          
                          species_name: The name of different types of birds 
                                        (sorted in alphabetical order)
                          species_counts: Counts how many times the bird 
                                          appears in the list 
    '''
    
    # Counts how many times a species appears in the observed list
    species_dict = {}
    for species in observed_list:
        if species in species_dict:
            species_dict[species] += 1
        else:
            species_dict[species] = 1
            
    # Add the tuple of (species_name, species counts) in a list
    # Sort the tuples in alphabetical order of the species_name
    species_list = sorted(list(species_dict.items()))
   
    # Calculate the proportion of a species in observed_list
    simpson = 0
    for freq in species_dict.values():
        simpson += (freq / len(observed_list))**2

    # Calculate Simpson inverse index
    if simpson == 0:
        return (0, species_list)
    else:
        return (1 / simpson, species_list)
    
# DO NOT DELETE/EDIT THIS LINE OF CODE, AS IT IS USED TO PROVIDE ACCESS TO
# THE FUNCTIONS FROM Q1 AND Q2
from hidden import get_species_richness, get_species_evenness

def compare_diversity(observed_list, diversity_measure):
    '''This function compares measures of diversity across different sites 
    
    Arguments: 
        observed_list: a list of independent observations of birds 
                       (tuples consisting of species of bird, and its habitat)
        diversity_measure: a string describing the measure of diversity to 
                          be used in ranking the habitats 
                          ("richness" or "evenness")
        
    Return: 
          [(habitat, diversity value)]
          a list of tuples, with each tuple consisting of:
          1. the habitat name
          2. the diversity of that habitat according to the specified measure
    The list of tuples should be sorted from most diverse to least diverse 
    habitat, if the habitat has same level of diversity, the tuples will be 
    sorted alphabetically by the habitat names. 
    
    '''
    
    # Categorise each species under different habitats 
    habitat_dict = dict()
    for species, habitat in observed_list:
        if habitat in habitat_dict:
            habitat_dict[habitat].append(species)
        else:
            habitat_dict[habitat] = [species]

    # Use the diversity measure required (richness / evenness)
    
    results_list = []
    
    for habitat, species_list in habitat_dict.items(): 
        if diversity_measure == "richness":
            # Calculate the diversity measure for each habitat in the list
            diversity_value = get_species_richness(species_list)[0] 
        elif diversity_measure == "evenness":
            diversity_value = get_species_evenness(species_list)[0]
        results_list.append((habitat, diversity_value))
    
    # Sorting the tuples by the diversity measure by:
    # 1. Making the diversity measure negative 
    # 2. Swapping the diversity measure and habitat, as the first element of 
    #    tuple is sorted first, and then the second element will be 
    #    sorted alphabetically

    new_results_list = []
    
    for habitat, diversity_value in results_list:
        diversity_value = -1* diversity_value
        new_results_list.append((diversity_value, habitat))
        
    # Reversing the above operations, and return the results without negative 
    # numbers

    sorted_list = []
    
    for diversity_value, habitat in sorted(new_results_list):
        diversity_value = diversity_value * -1
        sorted_list.append((habitat, diversity_value))
    
    return sorted_list

    


def optimise_study(sample_data, unseen_species, consecutive_visits):
    '''This function evaluates the effect that consecutive visits and 
       unseen species thresholds have on the accuracy of diversity estimates
       
       Arguments: 
           sample_data: a list of lists of data collected over the course of 
                        multiple sampling visits; each item in the main list is 
                        a list of species that were observed on that visit;

            unseen_species:  an integer that represents the minimum number of 
                             previously unseen species that must be observed 
                             before a visit is deemed productive

            consecutive_visits: an integer of consecutive unproductive visits, 
                                after the initial visit, that must occur to 
                                trigger the stopping rule.
       
       Return: 
           (num_of_visits, proportion_observed)
           A tuple consists of: 
               num_of_visits: the number of visits that will occur before the 
                              study has stopped.
               
               proportion_observed: the proportion of the total bird species 
                                    observed by the study at that point, 
                                    compared to if all sampling visits 
                                    contained in sample_data had been 
                                    conducted.               
       '''
    
    species_set = set()
    unproductive_visits = 0
    visit_counts = 0
    
    if not sample_data:
        return (0, 0)
    
    else: 
        # Record the number of new found species in each visits
        for visit in sample_data: 
            # Update the total number of visits before stopped
            visit_counts += 1 
            new_species = 0
            for species in visit: 
                if species in species_set:
                    new_species = new_species
                    species_set = species_set
                elif species not in species_set:
                    species_set.add(species)
                    new_species += 1
        
            # Update the number of consecutive unproductive visits        
         
            if new_species < unseen_species:
                unproductive_visits += 1
            else: 
                unproductive_visits = 0

            # Check if the consecutive unproductive visits exceed the specified 
            # number (consecutive_visits)
            if unproductive_visits == consecutive_visits: 
                break 
    
        new_species_before_stopped = len(species_set)
    
        # Count the total number of species in sample data
        for i in range(visit_counts, len(sample_data)):
            for species in sample_data[i]: 
                if species in species_set:
                    species_set = species_set
                elif species not in species_set:
                    species_set.add(species)
    
        total_species = len(species_set)
    
        return visit_counts, new_species_before_stopped / total_species



def infer_bird_species(environment, observations, region_list):
    
    '''This function predicts the species likely to be observed in each region
       based on the given environment and observations of bird species.
    
    Argument: 
        environment: a list of lists of regions in the environment.
        observations: 
        region_list:
    
    Return: 
        [[Species in region_list (i,j)], [Species in region (i,j)]...]
        A list consists of: 
            predicted bird species for each of the regions in region_list
            (sorted)
    
    '''
    
    # Iterating through the environment lists and corresponding observation 
    # lists to find the environmental factors for each species 
    species_dict = dict()
    
    for i in range(len(environment)):
        for j in range(len(environment)):
            for species in observations[i][j]:
                for k in range(0,len(environment)):
                    if environment [i][j][k] == 1: 
                        environment [i][j][k] == k 
                    elif environment [i][j][k] == 0:
                        environment [i][j][k] == a
                
                species_dict.update({species:environment[i][j]})        
                if species not in species_dict:
                    
                elif species in species_dict:
                    
    # remove all the "0"s (replaced by a)
    # Adding species into dictionary and corresponding list
    

    
    # Turn lists of environment factors into set 
    set()
    
    # Using set to find the intersection between 
    for species in 
        if species not in species_dict:
        
                        
    
    # Using dictionary to predict the species in a region 
    results = []
    
    for i, j in region_list:
        curr_list = []
        # Predicts all the possible species appearing in this region
        for species, factors in species_dict.items():
            # if factors is subset of region_list
                # add species in to the predicted list
            if factors 
        
        results.append(curr_list)
